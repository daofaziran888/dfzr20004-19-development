"""卸货交接领域服务：关联运单和航次。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class DischargeService(BaseModuleService):
    MODULE = "discharge"
    ENTITY = "卸货单"
    OPERATION_TERM = "完成交接"
    LIST_FIELDS = ["卸货港口", "收货单位", "实卸重量", "交接时间", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["卸货港口", "收货单位", "实卸重量"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"完成交接": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["voyage_id", "cargo_manifest_id"]