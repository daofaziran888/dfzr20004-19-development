"""跨模块编排路由：提供端到端业务视图 API。"""
from __future__ import annotations

from fastapi import APIRouter

from app.services import pipeline

router = APIRouter(prefix="/api/pipeline", tags=["跨模块编排"])


@router.get("/voyage/{voyage_id}/full-track")
def voyage_full_track(voyage_id: int):
    """航次全程跟踪：船舶→航线→航次→过闸→运单→配载→加油→泊位→卸货→货损→规费→事件。"""
    return pipeline.voyage_full_track(voyage_id)


@router.get("/vessel/{vessel_id}/panorama")
def vessel_panorama(vessel_id: int):
    """船舶运营全景：某艘船的所有关联业务。"""
    return pipeline.vessel_operation_panorama(vessel_id)


@router.get("/damage/{damage_id}/trace")
def cargo_damage_trace(damage_id: int):
    """货损追溯链：运单→航次→配载→卸货→货损。"""
    return pipeline.cargo_damage_trace(damage_id)


@router.get("/route/{route_id}/safety")
def route_safety(route_id: int):
    """航线安全状态：水位监测 + 气象预警 + 禁限航。"""
    return pipeline.route_safety_status(route_id)


@router.get("/manifest/{manifest_id}/delivery-check")
def manifest_delivery_check(manifest_id: int):
    """运单装卸核验：运单→航次→卸货交接。"""
    return pipeline.manifest_delivery_check(manifest_id)