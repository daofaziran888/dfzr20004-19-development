"""船舶维保领域服务：关联船舶。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class MaintenanceService(BaseModuleService):
    MODULE = "maintenance"
    ENTITY = "维保记录"
    OPERATION_TERM = "安排维保"
    LIST_FIELDS = ["维保项目", "维保周期", "上次维保日", "下次到期", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["维保项目", "维保周期"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"安排维保": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["vessel_id"]