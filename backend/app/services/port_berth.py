"""港口泊位领域服务：关联船舶/航次。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class PortBerthService(BaseModuleService):
    MODULE = "port_berth"
    ENTITY = "泊位"
    OPERATION_TERM = "分配泊位"
    LIST_FIELDS = ["泊位编号", "靠泊能力", "当前占用", "空闲时段", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["泊位编号", "靠泊能力"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"分配泊位": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["vessel_id", "voyage_id"]