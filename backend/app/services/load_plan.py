"""配载方案领域服务：关联运单和航次，某船某航次如何配载。"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService
from app.store import store


class LoadPlanService(BaseModuleService):
    MODULE = "load_plan"
    ENTITY = "配载计划"
    OPERATION_TERM = "确认配载"
    LIST_FIELDS = ["装载顺序", "舱位分配", "稳性校验", "积载因数", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["装载顺序", "舱位分配"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"确认配载": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["voyage_id", "cargo_manifest_id"]

    def get_cargo_manifest(self, plan_id: int) -> dict[str, Any] | None:
        """获取配载方案关联的运单。"""
        entry = store.find("load_plan", plan_id)
        if entry and entry.get("cargo_manifest_id"):
            return store.find("cargo_manifest", entry["cargo_manifest_id"])
        return None