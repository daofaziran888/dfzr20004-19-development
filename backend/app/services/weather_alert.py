"""气象预警领域服务：关联航段。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class WeatherAlertService(BaseModuleService):
    MODULE = "weather_alert"
    ENTITY = "预警通知"
    OPERATION_TERM = "发布预警"
    LIST_FIELDS = ["预警类型", "影响航段", "预警等级", "有效时段", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["预警类型", "影响航段", "预警等级"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"发布预警": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["route_id"]