"""货物运单领域服务：关联航次，运单随某航次运输。"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService
from app.store import store


class CargoManifestService(BaseModuleService):
    MODULE = "cargo_manifest"
    ENTITY = "运单"
    OPERATION_TERM = "签收运单"
    LIST_FIELDS = ["货物品名", "托运重量", "装货港", "卸货港", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["货物品名", "托运重量", "装货港", "卸货港"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"签收运单": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["voyage_id"]

    def get_load_plans(self, manifest_id: int) -> list[dict[str, Any]]:
        """获取该运单的配载方案。"""
        return [r for r in store.rows("load_plan") if r.get("cargo_manifest_id") == manifest_id]

    def get_discharges(self, manifest_id: int) -> list[dict[str, Any]]:
        """获取该运单的卸货记录。"""
        return [r for r in store.rows("discharge") if r.get("cargo_manifest_id") == manifest_id]

    def get_cargo_damages(self, manifest_id: int) -> list[dict[str, Any]]:
        """获取该运单的货损记录。"""
        return [r for r in store.rows("cargo_damage") if r.get("cargo_manifest_id") == manifest_id]