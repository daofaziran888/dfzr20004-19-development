"""货损记录领域服务：关联运单和航次。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class CargoDamageService(BaseModuleService):
    MODULE = "cargo_damage"
    ENTITY = "货损报告"
    OPERATION_TERM = "上报货损"
    LIST_FIELDS = ["货损品名", "损毁程度", "发现时间", "责任认定", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["货损品名", "损毁程度", "发现时间"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"上报货损": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["voyage_id", "cargo_manifest_id"]