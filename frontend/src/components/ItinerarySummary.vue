<script setup lang="ts">
import type { BudgetSummary, Itinerary, PlanStatus, PublicExecutionSummary } from '../types/travel.ts'
import { categoryLabels, formatCostBasis, formatMoney } from '../utils/presentation.ts'
defineProps<{ itinerary?: Itinerary | null; basis?: BudgetSummary['basis']; status?: PlanStatus; execution?: PublicExecutionSummary | null }>()
</script>
<template>
  <section class="panel itinerary-panel" aria-labelledby="itinerary-title">
    <h3 id="itinerary-title">Itinerary</h3>
    <template v-if="itinerary">
      <div class="trip-heading"><div><p class="trip-destination">{{ itinerary.destination }}</p><p>{{ itinerary.days }}-day itinerary</p></div><div><p class="muted">Estimated trip cost · {{ formatCostBasis(basis) }}</p><strong class="trip-cost">{{ formatMoney(itinerary.estimated_total_cost, itinerary.currency) }}</strong></div></div>
      <p class="muted">Activity costs and day totals: {{ formatCostBasis(basis) }}.</p>
      <div class="day-list">
        <section v-for="day in itinerary.daily_plan" :key="day.day_number" class="day-card" :aria-labelledby="`day-${day.day_number}`">
          <header class="day-heading"><h4 :id="`day-${day.day_number}`">Day {{ day.day_number }}</h4><span class="muted">{{ day.activities.length }} planned items</span></header>
          <ul class="activity-list"><li v-for="(activity, index) in day.activities" :key="index"><div><strong>{{ activity.name }}</strong><span class="activity-category">{{ categoryLabels[activity.category] }}</span></div><span class="activity-cost">{{ formatMoney(activity.estimated_cost, itinerary.currency) }}</span></li></ul>
          <p v-if="!day.activities.length" class="muted">No activities reported for this day.</p>
          <div class="day-total"><span>Estimated day total</span><strong>{{ formatMoney(day.estimated_cost, itinerary.currency) }}</strong></div>
        </section>
      </div>
      <p v-if="!itinerary.daily_plan.length" class="muted">No day-by-day details reported.</p>
    </template>
    <div v-else class="result-empty">
      <strong>No itinerary produced</strong>
      <p v-if="status === 'needs_clarification'">Complete the required trip details to generate an itinerary.</p>
      <p v-else-if="execution?.tools.some(tool => tool.tool_name !== 'calculate_budget' && tool.executed && tool.status === 'NO_RESULTS')">Search tools returned no usable travel options, so no itinerary is available.</p>
      <p v-else>No itinerary available for this run.</p>
    </div>
  </section>
</template>
