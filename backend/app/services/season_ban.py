"""禁限航管理领域服务：关联航段。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class SeasonBanService(BaseModuleService):
    MODULE = "season_ban"
    ENTITY = "禁限航令"
    OPERATION_TERM = "发布禁令"
    LIST_FIELDS = ["禁航河段", "禁航原因", "开始时间", "结束时间", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["禁航河段", "禁航原因", "开始时间", "结束时间"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"发布禁令": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["route_id"]