"""过闸排班领域服务：关联航次，某航次在某船闸排班。"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService
from app.store import store


class LockBookingService(BaseModuleService):
    MODULE = "lock_booking"
    ENTITY = "过闸申请"
    OPERATION_TERM = "申报过闸"
    LIST_FIELDS = ["船闸名称", "申请通过时间", "排队序号", "预计等候", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["船闸名称", "申请通过时间"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"申报过闸": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    REF_FIELDS = ["voyage_id"]

    def get_voyage(self, booking_id: int) -> dict[str, Any] | None:
        """获取过闸申请关联的航次。"""
        entry = store.find("lock_booking", booking_id)
        if entry and entry.get("voyage_id"):
            return store.find("voyage", entry["voyage_id"])
        return None