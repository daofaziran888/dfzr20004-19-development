"""跨模块业务编排：航次全程跟踪链、船舶运营全景等跨模块数据流。

每个流水线从多个模块聚合数据，提供端到端业务视图：
- 航次全程跟踪：船舶→航线→航次→过闸→运单→配载→加油→泊位→卸货→货损→规费→事件
- 船舶运营全景：某艘船的所有关联业务（船员、航次、维保、加油、规费）
- 货损追溯链：运单→航次→配载→卸货→货损
- 水位/气象联动：航线→水位→气象→航次
"""
from __future__ import annotations

from typing import Any

from app.store import store


def _rows_by_field(module: str, field: str, value: Any) -> list[dict[str, Any]]:
    """通用辅助：按指定字段值筛选模块记录。"""
    return [
        row for row in store.rows(module)
        if row.get(field) == value or str(row.get(field, "")) == str(value)
    ]


def _find_one(module: str, entry_id: int) -> dict[str, Any] | None:
    return store.find(module, entry_id)


# ── 航次全程跟踪链 ───────────────────────────────────────────────────

def voyage_full_track(voyage_id: int) -> dict[str, Any]:
    """航次全程跟踪：从船舶、航线到卸货的完整链路。

    关联模块：vessel → route → voyage → lock_booking → cargo_manifest
    → load_plan → fuel_supply → port_berth → discharge → cargo_damage
    → toll_fee → incident_log → ais_track
    """
    voyage = _find_one("voyage", voyage_id)
    if not voyage:
        return {"found": False, "voyage_id": voyage_id, "chain": []}

    vessel_id = voyage.get("vessel_id")
    route_id = voyage.get("route_id")

    vessel = _find_one("vessel", vessel_id) if vessel_id else None
    route = _find_one("route", route_id) if route_id else None
    lock_bookings = _rows_by_field("lock_booking", "voyage_id", voyage_id)
    manifests = _rows_by_field("cargo_manifest", "voyage_id", voyage_id)
    load_plans = _rows_by_field("load_plan", "voyage_id", voyage_id)
    fuel_supplies = _rows_by_field("fuel_supply", "voyage_id", voyage_id)
    port_berths = _rows_by_field("port_berth", "voyage_id", voyage_id)
    discharges = _rows_by_field("discharge", "voyage_id", voyage_id)

    # 货损关联运单
    cargo_damages = []
    for m in manifests:
        cargo_damages.extend(_rows_by_field("cargo_damage", "cargo_manifest_id", m.get("id")))

    toll_fees = _rows_by_field("toll_fee", "voyage_id", voyage_id)
    incident_logs = _rows_by_field("incident_log", "voyage_id", voyage_id)
    ais_tracks = _rows_by_field("ais_track", "voyage_id", voyage_id)

    # 水位和气象关联航线
    water_gauges = _rows_by_field("water_gauge", "route_id", route_id) if route_id else []
    weather_alerts = _rows_by_field("weather_alert", "route_id", route_id) if route_id else []
    season_bans = _rows_by_field("season_ban", "route_id", route_id) if route_id else []

    chain = []
    if vessel:
        chain.append({"step": "船舶登记", "module": "vessel", "data": vessel})
    if route:
        chain.append({"step": "航线编排", "module": "route", "data": route})
    chain.append({"step": "航次计划", "module": "voyage", "data": voyage})
    for item in lock_bookings:
        chain.append({"step": "过闸排班", "module": "lock_booking", "data": item})
    for item in manifests:
        chain.append({"step": "货物运单", "module": "cargo_manifest", "data": item})
    for item in load_plans:
        chain.append({"step": "配载方案", "module": "load_plan", "data": item})
    for item in fuel_supplies:
        chain.append({"step": "燃油补给", "module": "fuel_supply", "data": item})
    for item in port_berths:
        chain.append({"step": "港口泊位", "module": "port_berth", "data": item})
    for item in discharges:
        chain.append({"step": "卸货交接", "module": "discharge", "data": item})
    for item in cargo_damages:
        chain.append({"step": "货损记录", "module": "cargo_damage", "data": item})
    for item in toll_fees:
        chain.append({"step": "规费结算", "module": "toll_fee", "data": item})
    for item in incident_logs:
        chain.append({"step": "航行事件", "module": "incident_log", "data": item})
    for item in ais_tracks:
        chain.append({"step": "航迹追踪", "module": "ais_track", "data": item})
    for item in water_gauges:
        chain.append({"step": "水位监测", "module": "water_gauge", "data": item})
    for item in weather_alerts:
        chain.append({"step": "气象预警", "module": "weather_alert", "data": item})
    for item in season_bans:
        chain.append({"step": "禁限航管理", "module": "season_ban", "data": item})

    return {
        "found": True,
        "voyage_id": voyage_id,
        "vessel_id": vessel_id,
        "route_id": route_id,
        "summary": {
            "vessel_name": vessel.get("船名", "—") if vessel else "—",
            "route_from": route.get("起点港", "—") if route else "—",
            "route_to": route.get("终点港", "—") if route else "—",
            "voyage_no": voyage.get("航次编号", "—"),
            "step_count": len(chain),
        },
        "chain": chain,
    }


# ── 船舶运营全景 ─────────────────────────────────────────────────────

def vessel_operation_panorama(vessel_id: int) -> dict[str, Any]:
    """某艘船的所有关联业务：船员、航次、维保、加油、规费。"""
    vessel = _find_one("vessel", vessel_id)
    if not vessel:
        return {"found": False, "vessel_id": vessel_id}

    crew = _rows_by_field("crew", "vessel_id", vessel_id)
    voyages = _rows_by_field("voyage", "vessel_id", vessel_id)
    maintenances = _rows_by_field("maintenance", "vessel_id", vessel_id)
    fuel_supplies = _rows_by_field("fuel_supply", "vessel_id", vessel_id)
    toll_fees = _rows_by_field("toll_fee", "vessel_id", vessel_id)
    port_berths = _rows_by_field("port_berth", "vessel_id", vessel_id)

    return {
        "found": True,
        "vessel_id": vessel_id,
        "vessel_name": vessel.get("船名", "—"),
        "vessel_type": vessel.get("船舶类型", "—"),
        "crew": [{"id": c.get("id"), "name": c.get("船员姓名"), "role": c.get("在船职务")} for c in crew],
        "voyages": [{"id": v.get("id"), "no": v.get("航次编号"), "status": v.get("status")} for v in voyages],
        "maintenance": [{"id": m.get("id"), "item": m.get("维保项目"), "due": m.get("下次到期")} for m in maintenances],
        "fuel_supplies": [{"id": f.get("id"), "grade": f.get("油品标号"), "port": f.get("补给港口")} for f in fuel_supplies],
        "toll_fees": [{"id": t.get("id"), "type": t.get("费用类型"), "amount": t.get("应缴金额")} for t in toll_fees],
        "port_berths": [{"id": p.get("id"), "berth_no": p.get("泊位编号")} for p in port_berths],
    }


# ── 货损追溯链 ───────────────────────────────────────────────────────

def cargo_damage_trace(damage_id: int) -> dict[str, Any]:
    """从货损记录出发，追溯：运单→航次→配载→卸货。"""
    damage = _find_one("cargo_damage", damage_id)
    if not damage:
        return {"found": False, "damage_id": damage_id}

    manifest_id = damage.get("cargo_manifest_id")
    voyage_id = damage.get("voyage_id")

    manifest = _find_one("cargo_manifest", manifest_id) if manifest_id else None
    voyage = _find_one("voyage", voyage_id) if voyage_id else None
    load_plans = _rows_by_field("load_plan", "voyage_id", voyage_id) if voyage_id else []
    discharges = _rows_by_field("discharge", "voyage_id", voyage_id) if voyage_id else []

    return {
        "found": True,
        "damage_id": damage_id,
        "goods_name": damage.get("货损品名", "—"),
        "damage_level": damage.get("损毁程度", "—"),
        "manifest": {"id": manifest.get("id"), "goods": manifest.get("货物品名")} if manifest else None,
        "voyage": {"id": voyage.get("id"), "no": voyage.get("航次编号")} if voyage else None,
        "load_plans": [{"id": lp.get("id"), "order": lp.get("装载顺序")} for lp in load_plans],
        "discharges": [{"id": d.get("id"), "port": d.get("卸货港口"), "weight": d.get("实卸重量")} for d in discharges],
    }


# ── 航线水位气象联动 ─────────────────────────────────────────────────

def route_safety_status(route_id: int) -> dict[str, Any]:
    """航线安全状态：水位监测 + 气象预警 + 禁限航。"""
    route = _find_one("route", route_id)
    if not route:
        return {"found": False, "route_id": route_id}

    water_gauges = _rows_by_field("water_gauge", "route_id", route_id)
    weather_alerts = _rows_by_field("weather_alert", "route_id", route_id)
    season_bans = _rows_by_field("season_ban", "route_id", route_id)

    has_warning = any(w.get("当前水位", "") == "超警戒" for w in water_gauges)
    has_alert = any(a.get("status") == "已确认" for a in weather_alerts)
    has_ban = any(b.get("status") == "已确认" for b in season_bans)

    return {
        "found": True,
        "route_id": route_id,
        "route_from": route.get("起点港", "—"),
        "route_to": route.get("终点港", "—"),
        "safe_to_navigate": not (has_warning or has_alert or has_ban),
        "water_gauges": water_gauges,
        "weather_alerts": weather_alerts,
        "season_bans": season_bans,
        "warnings": [
            *(f"水位超警戒: {w.get('监测站点')}" for w in water_gauges if w.get('当前水位') == '超警戒'),
            *(f"气象预警: {a.get('预警类型')}-{a.get('预警等级')}" for a in weather_alerts if a.get('status') == '已确认'),
            *(f"禁限航: {b.get('禁航河段')}" for b in season_bans if b.get('status') == '已确认'),
        ],
    }


# ── 运单卸货交接核验 ─────────────────────────────────────────────────

def manifest_delivery_check(manifest_id: int) -> dict[str, Any]:
    """运单装卸核验：运单→航次→卸货交接。"""
    manifest = _find_one("cargo_manifest", manifest_id)
    if not manifest:
        return {"found": False, "manifest_id": manifest_id}

    voyage_id = manifest.get("voyage_id")
    voyage = _find_one("voyage", voyage_id) if voyage_id else None
    discharges = _rows_by_field("discharge", "cargo_manifest_id", manifest_id)
    load_plans = _rows_by_field("load_plan", "cargo_manifest_id", manifest_id)

    total_discharged = sum(
        float(d.get("实卸重量", 0)) if isinstance(d.get("实卸重量"), (int, float)) else 0
        for d in discharges
    )
    shipped = float(manifest.get("托运重量", 0)) if isinstance(manifest.get("托运重量"), (int, float)) else 0

    return {
        "found": True,
        "manifest_id": manifest_id,
        "goods": manifest.get("货物品名", "—"),
        "shipped_weight": shipped,
        "total_discharged": total_discharged,
        "weight_match": abs(total_discharged - shipped) < 0.01 if shipped > 0 else True,
        "voyage": {"id": voyage.get("id"), "no": voyage.get("航次编号")} if voyage else None,
        "load_plans": load_plans,
        "discharges": discharges,
    }