<template>
  <div class="app-shell">
    <aside class="app-side">
      <h1 class="app-title">内河航运调度中心</h1>
      <nav class="nav-list">
        <RouterLink v-for="item in navItems" :key="item.path" :to="item.path" class="nav-item">
          {{ item.label }}
        </RouterLink>
      </nav>
    </aside>
    <main class="app-main">
      <header class="app-head">
        <span class="head-desc">船东、船长和调度员共同编排航次计划、过闸排班与货物周转，按同一份运单完成从装港到卸港的全程跟踪。</span>
        <span class="head-user">当前值班：应用开发组</span>
      </header>
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
const navItems = [{ label: "运营概览", path: "/" }, { label: "船舶登记", path: "/vessel" }, { label: "船员调配", path: "/crew" }, { label: "航线编排", path: "/route" }, { label: "航次计划", path: "/voyage" }, { label: "过闸排班", path: "/lock_booking" }, { label: "货物运单", path: "/cargo_manifest" }, { label: "配载方案", path: "/load_plan" }, { label: "燃油补给", path: "/fuel_supply" }, { label: "港口泊位", path: "/port_berth" }, { label: "水位监测", path: "/water_gauge" }, { label: "气象预警", path: "/weather_alert" }, { label: "货损记录", path: "/cargo_damage" }, { label: "船舶维保", path: "/maintenance" }, { label: "规费结算", path: "/toll_fee" }, { label: "航迹追踪", path: "/ais_track" }, { label: "航行事件", path: "/incident_log" }, { label: "卸货交接", path: "/discharge" }, { label: "禁限航管理", path: "/season_ban" }]
</script>
