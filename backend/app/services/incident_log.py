"""航行事件领域服务：关联航次和航段（route）。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class IncidentLogService(BaseModuleService):
    MODULE = "incident_log"
    ENTITY = "事件日志"
    OPERATION_TERM = "上报事件"
    LIST_FIELDS = ["事件类型", "发生航段", "涉事船舶", "处置结果", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["事件类型", "发生航段", "涉事船舶"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"上报事件": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["voyage_id", "route_id"]