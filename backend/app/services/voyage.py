"""航次计划领域服务：关联船舶、航线，是跨模块数据流的核心枢纽。"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService
from app.store import store


class VoyageService(BaseModuleService):
    MODULE = "voyage"
    ENTITY = "航次"
    OPERATION_TERM = "排定航次"
    LIST_FIELDS = ["航次编号", "计划开航", "预计到达", "承运货类", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["航次编号", "计划开航", "预计到达"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"排定航次": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["vessel_id", "route_id"]

    def get_lock_bookings(self, voyage_id: int) -> list[dict[str, Any]]:
        """获取该航次的过闸排班。"""
        return [r for r in store.rows("lock_booking") if r.get("voyage_id") == voyage_id]

    def get_cargo_manifests(self, voyage_id: int) -> list[dict[str, Any]]:
        """获取该航次的货物运单。"""
        return [r for r in store.rows("cargo_manifest") if r.get("voyage_id") == voyage_id]

    def get_load_plans(self, voyage_id: int) -> list[dict[str, Any]]:
        """获取该航次的配载方案。"""
        return [r for r in store.rows("load_plan") if r.get("voyage_id") == voyage_id]

    def get_fuel_supplies(self, voyage_id: int) -> list[dict[str, Any]]:
        """获取该航次的燃油补给。"""
        return [r for r in store.rows("fuel_supply") if r.get("voyage_id") == voyage_id]

    def get_port_berths(self, voyage_id: int) -> list[dict[str, Any]]:
        """获取该航次的港口泊位。"""
        return [r for r in store.rows("port_berth") if r.get("voyage_id") == voyage_id]

    def get_discharges(self, voyage_id: int) -> list[dict[str, Any]]:
        """获取该航次的卸货记录。"""
        return [r for r in store.rows("discharge") if r.get("voyage_id") == voyage_id]

    def get_incident_logs(self, voyage_id: int) -> list[dict[str, Any]]:
        """获取该航次的航行事件。"""
        return [r for r in store.rows("incident_log") if r.get("voyage_id") == voyage_id]

    def get_ais_tracks(self, voyage_id: int) -> list[dict[str, Any]]:
        """获取该航次的航迹。"""
        return [r for r in store.rows("ais_track") if r.get("voyage_id") == voyage_id]

    def get_toll_fees(self, voyage_id: int) -> list[dict[str, Any]]:
        """获取该航次的规费。"""
        return [r for r in store.rows("toll_fee") if r.get("voyage_id") == voyage_id]

    def get_cargo_damages(self, voyage_id: int) -> list[dict[str, Any]]:
        """获取该航次的货损记录。"""
        return [r for r in store.rows("cargo_damage") if r.get("voyage_id") == voyage_id]