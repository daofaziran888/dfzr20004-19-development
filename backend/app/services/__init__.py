"""领域服务注册表：通用资源路由按模块 key 分派到独立业务服务。"""
from __future__ import annotations

from app.services.base import BaseModuleService
from app.services.vessel import VesselService
from app.services.crew import CrewService
from app.services.route import RouteService
from app.services.voyage import VoyageService
from app.services.lock_booking import LockBookingService
from app.services.cargo_manifest import CargoManifestService
from app.services.load_plan import LoadPlanService
from app.services.fuel_supply import FuelSupplyService
from app.services.port_berth import PortBerthService
from app.services.water_gauge import WaterGaugeService
from app.services.weather_alert import WeatherAlertService
from app.services.cargo_damage import CargoDamageService
from app.services.maintenance import MaintenanceService
from app.services.toll_fee import TollFeeService
from app.services.ais_track import AisTrackService
from app.services.incident_log import IncidentLogService
from app.services.discharge import DischargeService
from app.services.season_ban import SeasonBanService

SERVICES: dict[str, BaseModuleService] = {
    "vessel": VesselService(),
    "crew": CrewService(),
    "route": RouteService(),
    "voyage": VoyageService(),
    "lock_booking": LockBookingService(),
    "cargo_manifest": CargoManifestService(),
    "load_plan": LoadPlanService(),
    "fuel_supply": FuelSupplyService(),
    "port_berth": PortBerthService(),
    "water_gauge": WaterGaugeService(),
    "weather_alert": WeatherAlertService(),
    "cargo_damage": CargoDamageService(),
    "maintenance": MaintenanceService(),
    "toll_fee": TollFeeService(),
    "ais_track": AisTrackService(),
    "incident_log": IncidentLogService(),
    "discharge": DischargeService(),
    "season_ban": SeasonBanService(),
}


def service_for(module: str) -> BaseModuleService | None:
    return SERVICES.get(module)
