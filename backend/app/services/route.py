"""航线编排领域服务：关联水位、气象、禁限航。"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService
from app.store import store


class RouteService(BaseModuleService):
    MODULE = "route"
    ENTITY = "航线"
    OPERATION_TERM = "核定航线"
    LIST_FIELDS = ["起点港", "终点港", "航程公里", "通航等级", "登记编号", "负责人", "生效版本", "备注说明"]
    REQUIRED_FIELDS = ["起点港", "终点港", "航程公里"]
    STATUS_ORDER = ["草稿", "待确认", "已确认", "已撤回"]
    ACTION_RULES = {"核定航线": "已确认", "提交确认": "待确认", "撤回记录": "已撤回"}
    NEGATIVE_ACTIONS = []

    def get_voyages(self, route_id: int) -> list[dict[str, Any]]:
        """获取该航线的所有航次。"""
        return [r for r in store.rows("voyage") if r.get("route_id") == route_id]

    def get_water_gauges(self, route_id: int) -> list[dict[str, Any]]:
        """获取该航线的水位监测记录。"""
        return [r for r in store.rows("water_gauge") if r.get("route_id") == route_id]

    def get_weather_alerts(self, route_id: int) -> list[dict[str, Any]]:
        """获取该航线的气象预警。"""
        return [r for r in store.rows("weather_alert") if r.get("route_id") == route_id]

    def get_season_bans(self, route_id: int) -> list[dict[str, Any]]:
        """获取该航线的禁限航令。"""
        return [r for r in store.rows("season_ban") if r.get("route_id") == route_id]