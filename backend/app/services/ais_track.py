"""航迹追踪领域服务：关联航次。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class AisTrackService(BaseModuleService):
    MODULE = "ais_track"
    ENTITY = "位置报告"
    OPERATION_TERM = "记录位置"
    LIST_FIELDS = ["经度", "纬度", "航速节", "航向角度", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["经度", "纬度"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"记录位置": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["voyage_id", "vessel_id"]