<template>
  <section class="page">
    <header class="page-head">
      <div>
        <h2>运营概览</h2>
        <p class="page-desc">汇总各业务模块的关键指标，先看总量再看异常。</p>
      </div>
    </header>
    <div class="stat-row">
      <article v-for="card in cards" :key="card.label" class="stat-card">
        <span class="stat-label">{{ card.label }}</span>
        <strong class="stat-value">{{ card.value }}</strong>
      </article>
    </div>
    <table class="data-table">
      <thead>
        <tr><th>业务模块</th><th>今日新增</th><th>待处理</th><th>异常量</th></tr>
      </thead>
      <tbody>
        <tr v-for="row in moduleRows" :key="row.name">
          <td>{{ row.name }}</td>
          <td>{{ row.created }}</td>
          <td>{{ row.pending }}</td>
          <td>{{ row.abnormal }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { fetchJson } from '@/api/client'

type Overview = {
  cards: { label: string; value: number }[]
  modules: { name: string; created: number; pending: number; abnormal: number }[]
}

const cards = ref<Overview['cards']>([])
const moduleRows = ref<Overview['modules']>([])

onMounted(async () => {
  try {
    const payload = await fetchJson<Overview>('/api/overview')
    cards.value = payload.cards
    moduleRows.value = payload.modules
  } catch {
    cards.value = [{"label": "业务模块", "value": 0}, {"label": "今日新增", "value": 0}]
    moduleRows.value = [{"name": "船舶登记", "created": 0, "pending": 0, "abnormal": 0}, {"name": "船员调配", "created": 0, "pending": 0, "abnormal": 0}, {"name": "航线编排", "created": 0, "pending": 0, "abnormal": 0}, {"name": "航次计划", "created": 0, "pending": 0, "abnormal": 0}, {"name": "过闸排班", "created": 0, "pending": 0, "abnormal": 0}, {"name": "货物运单", "created": 0, "pending": 0, "abnormal": 0}, {"name": "配载方案", "created": 0, "pending": 0, "abnormal": 0}, {"name": "燃油补给", "created": 0, "pending": 0, "abnormal": 0}, {"name": "港口泊位", "created": 0, "pending": 0, "abnormal": 0}, {"name": "水位监测", "created": 0, "pending": 0, "abnormal": 0}, {"name": "气象预警", "created": 0, "pending": 0, "abnormal": 0}, {"name": "货损记录", "created": 0, "pending": 0, "abnormal": 0}, {"name": "船舶维保", "created": 0, "pending": 0, "abnormal": 0}, {"name": "规费结算", "created": 0, "pending": 0, "abnormal": 0}, {"name": "航迹追踪", "created": 0, "pending": 0, "abnormal": 0}, {"name": "航行事件", "created": 0, "pending": 0, "abnormal": 0}, {"name": "卸货交接", "created": 0, "pending": 0, "abnormal": 0}, {"name": "禁限航管理", "created": 0, "pending": 0, "abnormal": 0}]
  }
})
</script>
