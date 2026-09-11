<script setup lang="ts">
import { computed } from 'vue'
import type { TravelRequirements } from '../types/travel.ts'
import { formatEnumLabel, formatMoney, requirementState } from '../utils/presentation.ts'
const props = defineProps<{ requirements: TravelRequirements; missingFields: string[] }>()
const fields: [keyof TravelRequirements, string][] = [
  ['destination', 'Destination'], ['origin', 'Origin'], ['start_date', 'Start date'], ['end_date', 'End date'],
  ['duration_days', 'Duration'], ['travelers', 'Travelers'], ['budget_amount', 'Budget'], ['budget_scope', 'Budget scope'],
  ['currency', 'Currency'], ['interests', 'Interests'], ['hotel_preferences', 'Hotel preferences'],
  ['food_preferences', 'Food preferences'], ['transport_preferences', 'Transport preferences'], ['constraints', 'Extracted constraints'],
]
const rows = computed(() => fields.map(([key, label]) => {
  const value = props.requirements[key]
  const state = requirementState(key, value, props.missingFields)
  const display = state === 'missing' ? 'MISSING — required' : state === 'empty' ? 'None supplied'
    : state === 'absent' ? 'Not supplied' : key === 'budget_amount' ? formatMoney(value as number, props.requirements.currency)
      : key === 'budget_scope' ? formatEnumLabel(value as string) : key === 'duration_days' ? `${value} days` : value
  return { key, label, state, display }
}))
</script>
<template>
  <section class="panel" aria-labelledby="requirements-title">
    <h3 id="requirements-title">Extracted requirements</h3>
    <dl class="requirements-grid">
      <div v-for="row in rows" :key="row.key" :class="['requirement', row.state]">
        <dt>{{ row.label }}</dt>
        <dd><ul v-if="Array.isArray(row.display)" class="tags"><li v-for="(value, index) in row.display" :key="index">{{ value }}</li></ul><template v-else>{{ row.display }}</template></dd>
      </div>
    </dl>
    <p class="muted">Fields reflect the backend parser, including defaults such as currency. Missing optional fields are not errors.</p>
    <p v-if="requirements.constraints?.length" class="info-note">Constraints are extracted from the request; not all are enforced by the current demo planner.</p>
  </section>
</template>
