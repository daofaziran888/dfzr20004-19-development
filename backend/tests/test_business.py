"""跨模块业务数据链路测试：验证至少两个模块间的完整数据流。

每个测试从创建跨模块关联记录开始，到查询验证关联链结束。
使用 FastAPI TestClient 走完整 HTTP 请求-响应流程。
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _create(module: str, fields: dict) -> int:
    """创建一条记录，返回 id。"""
    payload = {"values": fields}
    resp = client.post(f"/api/{module}", json=payload)
    assert resp.status_code == 200, f"创建 {module} 失败: {resp.text}"
    data = resp.json()
    assert data["ok"], f"创建 {module}: {data.get('message')}"
    return data["entry"]["id"]


def _get(module: str, entry_id: int) -> dict:
    """获取一条记录。"""
    resp = client.get(f"/api/{module}/{entry_id}")
    assert resp.status_code == 200, f"获取 {module}/{entry_id} 失败: {resp.text}"
    return resp.json()


def _action(module: str, entry_id: int, action: str) -> dict:
    """对记录执行动作。"""
    resp = client.post(f"/api/{module}/{entry_id}/actions", json={"action": action})
    assert resp.status_code == 200
    return resp.json()


# ── 测试 1: 船舶→船员关联链 ──────────────────────────────────────────

def test_vessel_crew_link():
    """创建船舶 → 创建船员关联到该船 → 验证关联。"""
    vessel_id = _create("vessel", {
        "船名": "测试船001", "船舶类型": "散货船", "载重吨位": "3000吨",
    })
    vessel = _get("vessel", vessel_id)
    assert vessel["船名"] == "测试船001"

    crew_id = _create("crew", {
        "船员姓名": "测试船员A", "适任证书": "证-001", "在船职务": "船长",
        "vessel_id": vessel_id,
    })
    crew = _get("crew", crew_id)
    assert crew["船员姓名"] == "测试船员A"
    assert crew.get("vessel_id") == vessel_id

    # 通过 vessel service 查询船员
    from app.services.vessel import VesselService
    svc = VesselService()
    crew_list = svc.get_crew(vessel_id)
    assert len(crew_list) > 0
    assert any(c["id"] == crew_id for c in crew_list)


# ── 测试 2: 船舶→航线→航次关联链 ────────────────────────────────────

def test_vessel_route_voyage_triple_link():
    """创建船舶 + 航线 → 创建航次关联两者 → 验证三种关联。"""
    vessel_id = _create("vessel", {
        "船名": "测试船002", "船舶类型": "集装箱船", "载重吨位": "4000吨",
    })
    route_id = _create("route", {
        "起点港": "测试起运港", "终点港": "测试目的港", "航程公里": "800公里",
    })

    voyage_id = _create("voyage", {
        "航次编号": "TEST-VOY-002", "计划开航": "2026-12-01", "预计到达": "2026-12-10",
        "vessel_id": vessel_id, "route_id": route_id,
    })

    voyage = _get("voyage", voyage_id)
    assert voyage["航次编号"] == "TEST-VOY-002"
    assert voyage.get("vessel_id") == vessel_id
    assert voyage.get("route_id") == route_id

    # 验证船舶上有该航次
    from app.services.vessel import VesselService
    svc = VesselService()
    voyages = svc.get_voyages(vessel_id)
    assert any(v["id"] == voyage_id for v in voyages)

    # 验证航线可查到水位
    from app.services.route import RouteService
    route_svc = RouteService()
    water_gauges = route_svc.get_water_gauges(route_id)
    assert isinstance(water_gauges, list)


# ── 测试 3: 航次→过闸排班关联链 ──────────────────────────────────────

def test_voyage_lock_booking_link():
    """创建航次 → 创建过闸排班关联该航次 → 验证。"""
    # 先创建依赖
    vessel_id = _create("vessel", {
        "船名": "测试船003", "船舶类型": "散货船", "载重吨位": "3500吨",
    })
    route_id = _create("route", {
        "起点港": "三峡港", "终点港": "汉口港", "航程公里": "600公里",
    })
    voyage_id = _create("voyage", {
        "航次编号": "TEST-VOY-003", "计划开航": "2026-12-05", "预计到达": "2026-12-08",
        "vessel_id": vessel_id, "route_id": route_id,
    })

    lock_id = _create("lock_booking", {
        "船闸名称": "三峡船闸", "申请通过时间": "2026-12-06", "voyage_id": voyage_id,
    })
    lock = _get("lock_booking", lock_id)
    assert lock["船闸名称"] == "三峡船闸"
    assert lock.get("voyage_id") == voyage_id

    # 通过 voyage service 查询过闸
    from app.services.voyage import VoyageService
    vs = VoyageService()
    locks = vs.get_lock_bookings(voyage_id)
    assert any(l["id"] == lock_id for l in locks)


# ── 测试 4: 航次→货物运单→配载方案链 ────────────────────────────────

def test_voyage_manifest_loadplan_chain():
    """航次→运单→配载方案完整装货链。"""
    vessel_id = _create("vessel", {
        "船名": "测试船004", "船舶类型": "散货船", "载重吨位": "5000吨",
    })
    route_id = _create("route", {
        "起点港": "装货港", "终点港": "卸货港", "航程公里": "500公里",
    })
    voyage_id = _create("voyage", {
        "航次编号": "TEST-VOY-004", "计划开航": "2026-12-10", "预计到达": "2026-12-15",
        "vessel_id": vessel_id, "route_id": route_id,
    })

    manifest_id = _create("cargo_manifest", {
        "货物品名": "测试煤炭", "托运重量": "4000", "装货港": "装货港", "卸货港": "卸货港",
        "voyage_id": voyage_id,
    })
    manifest = _get("cargo_manifest", manifest_id)
    assert manifest["货物品名"] == "测试煤炭"
    assert manifest.get("voyage_id") == voyage_id

    load_id = _create("load_plan", {
        "装载顺序": "先煤", "舱位分配": "1号舱4000吨",
        "voyage_id": voyage_id, "cargo_manifest_id": manifest_id,
    })
    load = _get("load_plan", load_id)
    assert load.get("voyage_id") == voyage_id
    assert load.get("cargo_manifest_id") == manifest_id

    # 通过 cargo_manifest service 查配载
    from app.services.cargo_manifest import CargoManifestService
    cs = CargoManifestService()
    plans = cs.get_load_plans(manifest_id)
    assert any(p["id"] == load_id for p in plans)


# ── 测试 5: 船舶→航次→燃油补给链 ────────────────────────────────────

def test_vessel_voyage_fuel_chain():
    """船舶→航次→燃油补给完整燃料管理链。"""
    vessel_id = _create("vessel", {
        "船名": "测试船005", "船舶类型": "油船", "载重吨位": "8000吨",
    })
    route_id = _create("route", {
        "起点港": "南京港", "终点港": "上海港", "航程公里": "350公里",
    })
    voyage_id = _create("voyage", {
        "航次编号": "TEST-VOY-005", "计划开航": "2026-12-10", "预计到达": "2026-12-12",
        "vessel_id": vessel_id, "route_id": route_id,
    })

    fuel_id = _create("fuel_supply", {
        "油品标号": "0号柴油", "加油数量": "200", "补给港口": "镇江港",
        "vessel_id": vessel_id, "voyage_id": voyage_id,
    })
    fuel = _get("fuel_supply", fuel_id)
    assert fuel["油品标号"] == "0号柴油"
    assert fuel.get("vessel_id") == vessel_id
    assert fuel.get("voyage_id") == voyage_id

    # 通过 vessel service 查加油记录
    from app.services.vessel import VesselService
    svc = VesselService()
    fuels = svc.get_fuel_supplies(vessel_id)
    assert any(f["id"] == fuel_id for f in fuels)


# ── 测试 6: 航次→运单→卸货链 ────────────────────────────────────────

def test_voyage_manifest_discharge_chain():
    """货物运单→航次→卸货交接完整运输链。"""
    vessel_id = _create("vessel", {
        "船名": "测试船006", "船舶类型": "散货船", "载重吨位": "6000吨",
    })
    route_id = _create("route", {
        "起点港": "起运港A", "终点港": "目的港B", "航程公里": "1000公里",
    })
    voyage_id = _create("voyage", {
        "航次编号": "TEST-VOY-006", "计划开航": "2026-12-01", "预计到达": "2026-12-08",
        "vessel_id": vessel_id, "route_id": route_id,
    })
    manifest_id = _create("cargo_manifest", {
        "货物品名": "测试钢材", "托运重量": "3500", "装货港": "起运港A", "卸货港": "目的港B",
        "voyage_id": voyage_id,
    })

    discharge_id = _create("discharge", {
        "卸货港口": "目的港B", "收货单位": "测试收货方", "实卸重量": "3500",
        "voyage_id": voyage_id, "cargo_manifest_id": manifest_id,
    })
    discharge = _get("discharge", discharge_id)
    assert discharge["卸货港口"] == "目的港B"
    assert discharge.get("voyage_id") == voyage_id
    assert discharge.get("cargo_manifest_id") == manifest_id

    # 通过 cargo_manifest service 查卸货
    from app.services.cargo_manifest import CargoManifestService
    cs = CargoManifestService()
    discharges = cs.get_discharges(manifest_id)
    assert any(d["id"] == discharge_id for d in discharges)


# ── 测试 7: 运单→货损追溯链 ─────────────────────────────────────────

def test_manifest_damage_trace():
    """运单→航次→货损完整追溯链。"""
    vessel_id = _create("vessel", {
        "船名": "测试船007", "船舶类型": "集装箱船", "载重吨位": "4000吨",
    })
    route_id = _create("route", {
        "起点港": "始发港", "终点港": "终点港", "航程公里": "700公里",
    })
    voyage_id = _create("voyage", {
        "航次编号": "TEST-VOY-007", "计划开航": "2026-12-05", "预计到达": "2026-12-12",
        "vessel_id": vessel_id, "route_id": route_id,
    })
    manifest_id = _create("cargo_manifest", {
        "货物品名": "测试电子产品", "托运重量": "2000", "装货港": "始发港", "卸货港": "终点港",
        "voyage_id": voyage_id,
    })

    damage_id = _create("cargo_damage", {
        "货损品名": "测试电子产品", "损毁程度": "轻微", "发现时间": "2026-12-10",
        "voyage_id": voyage_id, "cargo_manifest_id": manifest_id,
    })
    damage = _get("cargo_damage", damage_id)
    assert damage["货损品名"] == "测试电子产品"
    assert damage.get("voyage_id") == voyage_id
    assert damage.get("cargo_manifest_id") == manifest_id

    # 通过 pipeline 追溯
    from app.services.pipeline import cargo_damage_trace
    trace = cargo_damage_trace(damage_id)
    assert trace["found"]
    assert trace["manifest"]["id"] == manifest_id
    assert trace["voyage"]["id"] == voyage_id


# ── 测试 8: 航线安全联动（水位+气象+禁限航） ─────────────────────────

def test_route_safety_multi_module():
    """航线关联水位监测+气象预警+禁限航→验证联动。"""
    route_id = _create("route", {
        "起点港": "安全港A", "终点港": "安全港B", "航程公里": "300公里",
    })

    water_id = _create("water_gauge", {
        "监测站点": "安全站A", "当前水位": "超警戒", "警戒水位": "50m",
        "route_id": route_id,
    })
    weather_id = _create("weather_alert", {
        "预警类型": "大风", "影响航段": "安全段", "预警等级": "红色",
        "route_id": route_id,
    })
    _action("weather_alert", weather_id, "发布预警")
    ban_id = _create("season_ban", {
        "禁航河段": "安全段", "禁航原因": "台风", "开始时间": "2026-12-01", "结束时间": "2026-12-05",
        "route_id": route_id,
    })
    _action("season_ban", ban_id, "发布禁令")

    # pipeline 安全状态
    from app.services.pipeline import route_safety_status
    status = route_safety_status(route_id)
    assert status["found"]
    assert not status["safe_to_navigate"]  # 有超警戒水位+预警+禁航
    assert len(status["warnings"]) >= 1


# ── 测试 9: 船舶运营全景 ─────────────────────────────────────────────

def test_vessel_operation_panorama():
    """某艘船的所有关联业务聚合。"""
    vessel_id = _create("vessel", {
        "船名": "全景船001", "船舶类型": "散货船", "载重吨位": "4500吨",
    })
    route_id = _create("route", {
        "起点港": "全景港", "终点港": "全景港B", "航程公里": "400公里",
    })
    # 创建多条关联
    _create("voyage", {
        "航次编号": "PANO-VOY-001", "计划开航": "2026-12-01", "预计到达": "2026-12-05",
        "vessel_id": vessel_id, "route_id": route_id,
    })
    _create("voyage", {
        "航次编号": "PANO-VOY-002", "计划开航": "2026-12-10", "预计到达": "2026-12-15",
        "vessel_id": vessel_id, "route_id": route_id,
    })
    _create("maintenance", {
        "维保项目": "主机检修", "维保周期": "12个月",
        "vessel_id": vessel_id,
    })
    _create("fuel_supply", {
        "油品标号": "0号柴油", "加油数量": "100", "补给港口": "全景补给港",
        "vessel_id": vessel_id, "voyage_id": None,
    })

    from app.services.pipeline import vessel_operation_panorama
    panorama = vessel_operation_panorama(vessel_id)
    assert panorama["found"]
    assert panorama["vessel_name"] == "全景船001"
    assert len(panorama["voyages"]) == 2
    assert len(panorama["maintenance"]) >= 1
    assert len(panorama["fuel_supplies"]) >= 1


# ── 测试 10: Pipeline 全程跟踪 ───────────────────────────────────────

def test_pipeline_voyage_full_track():
    """航次全程跟踪链：使用 seed 数据中的航次 1（长江之星）。"""
    from app.services.pipeline import voyage_full_track

    track = voyage_full_track(1)
    assert track["found"], f"航次1跟踪失败: {track}"
    assert track["voyage_id"] == 1
    assert track["summary"]["vessel_name"] == "长江之星01号"
    assert track["summary"]["route_from"] == "重庆朝天门"
    assert track["summary"]["route_to"] == "武汉阳逻港"
    assert track["summary"]["step_count"] >= 6  # 至少 vessel+route+voyage+lock+manifest+load_plan+fuel+port+discharge
    assert len(track["chain"]) >= 6

    # 验证链中有关键步骤
    steps = [s["module"] for s in track["chain"]]
    assert "vessel" in steps
    assert "route" in steps
    assert "voyage" in steps
    assert "lock_booking" in steps
    assert "cargo_manifest" in steps
    assert "load_plan" in steps


# ── 测试 11: 运单装卸核验 ─────────────────────────────────────────────

def test_manifest_delivery_check():
    """运单装卸核验：seed数据中运单1（动力煤4500吨，卸货4495吨，扣水5吨）。"""
    from app.services.pipeline import manifest_delivery_check

    check = manifest_delivery_check(1)
    assert check["found"]
    assert check["goods"] == "动力煤"
    assert check["shipped_weight"] == 4500
    assert check["total_discharged"] == 4495
    assert not check["weight_match"]  # 差了5吨
    assert check["voyage"] is not None
    assert len(check["discharges"]) >= 1
    assert len(check["load_plans"]) >= 1


# ── 测试 12: 状态流转 +跨模块联合查询 ─────────────────────────────────

def test_status_flow_with_cross_ref():
    """创建带跨模块引用的记录 → 执行状态流转 → 验证引用保持。"""
    vessel_id = _create("vessel", {
        "船名": "流转测试船", "船舶类型": "油船", "载重吨位": "7000吨",
    })
    route_id = _create("route", {
        "起点港": "流转港A", "终点港": "流转港B", "航程公里": "200公里",
    })
    voyage_id = _create("voyage", {
        "航次编号": "FLOW-VOY-001", "计划开航": "2026-12-01", "预计到达": "2026-12-03",
        "vessel_id": vessel_id, "route_id": route_id,
    })

    # 状态流转
    _action("voyage", voyage_id, "排定航次")
    voyage = _get("voyage", voyage_id)
    assert voyage["status"] == "已确认"
    # 验证跨模块引用未丢失
    assert voyage.get("vessel_id") == vessel_id
    assert voyage.get("route_id") == route_id

    # 撤回
    _action("voyage", voyage_id, "撤回记录")
    voyage = _get("voyage", voyage_id)
    assert voyage["status"] == "已撤回"
    assert voyage.get("vessel_id") == vessel_id  # 引用仍保留