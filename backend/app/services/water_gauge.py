"""水位监测领域服务：关联航段/航线。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class WaterGaugeService(BaseModuleService):
    MODULE = "water_gauge"
    ENTITY = "水位记录"
    OPERATION_TERM = "记录水位"
    LIST_FIELDS = ["监测站点", "当前水位", "警戒水位", "观测时间", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["监测站点", "当前水位", "警戒水位"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"记录水位": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["route_id"]