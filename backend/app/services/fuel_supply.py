"""燃油补给领域服务：关联船舶和航次。"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService
from app.store import store


class FuelSupplyService(BaseModuleService):
    MODULE = "fuel_supply"
    ENTITY = "加油记录"
    OPERATION_TERM = "登记加油"
    LIST_FIELDS = ["油品标号", "加油数量", "补给港口", "加油日期", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["油品标号", "加油数量", "补给港口"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"登记加油": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["vessel_id", "voyage_id"]