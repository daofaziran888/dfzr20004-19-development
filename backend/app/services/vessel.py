"""船舶登记领域服务：船舶是核心枢纽，关联船员、航次、维保、加油、泊位。"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService
from app.store import store


class VesselService(BaseModuleService):
    MODULE = "vessel"
    ENTITY = "船舶"
    OPERATION_TERM = "核验船舶"
    LIST_FIELDS = ["船名", "船舶类型", "载重吨位", "船龄年限", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["船名", "船舶类型", "载重吨位"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"核验船舶": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    # ── 跨模块读操作 ──

    def get_crew(self, vessel_id: int) -> list[dict[str, Any]]:
        """获取该船的船员列表。"""
        return [r for r in store.rows("crew") if r.get("vessel_id") == vessel_id]

    def get_voyages(self, vessel_id: int) -> list[dict[str, Any]]:
        """获取该船的所有航次。"""
        return [r for r in store.rows("voyage") if r.get("vessel_id") == vessel_id]

    def get_maintenance(self, vessel_id: int) -> list[dict[str, Any]]:
        """获取该船的维保记录。"""
        return [r for r in store.rows("maintenance") if r.get("vessel_id") == vessel_id]

    def get_fuel_supplies(self, vessel_id: int) -> list[dict[str, Any]]:
        """获取该船的燃油补给记录。"""
        return [r for r in store.rows("fuel_supply") if r.get("vessel_id") == vessel_id]

    def get_toll_fees(self, vessel_id: int) -> list[dict[str, Any]]:
        """获取该船的规费账单。"""
        return [r for r in store.rows("toll_fee") if r.get("vessel_id") == vessel_id]