"""规费结算领域服务：关联航次/船舶。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class TollFeeService(BaseModuleService):
    MODULE = "toll_fee"
    ENTITY = "规费账单"
    OPERATION_TERM = "确认缴费"
    LIST_FIELDS = ["费用类型", "计费标准", "应缴金额", "缴费期限", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["费用类型", "应缴金额"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"确认缴费": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["voyage_id", "vessel_id"]