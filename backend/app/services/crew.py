"""船员调配领域服务：关联船舶，船员在某船任职。"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService
from app.store import store


class CrewService(BaseModuleService):
    MODULE = "crew"
    ENTITY = "船员"
    OPERATION_TERM = "调配船员"
    LIST_FIELDS = ["船员姓名", "适任证书", "在船职务", "上船日期", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["船员姓名", "适任证书", "在船职务"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"调配船员": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    # 跨模块：某船上的所有船员
    REF_FIELDS = ["vessel_id"]

    def get_vessel_crew(self, vessel_id: int) -> list[dict[str, Any]]:
        """获取某船的船员名单。"""
        return [r for r in store.rows("crew") if r.get("vessel_id") == vessel_id]