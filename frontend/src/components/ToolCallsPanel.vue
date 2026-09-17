<script setup lang="ts">
import type { PublicToolRecord, TravelRequirements } from '../types/travel.ts'
import { formatMoney } from '../utils/presentation.ts'
import ToolCallCard from './ToolCallCard.vue'
defineProps<{ tools: PublicToolRecord[]; requirements: TravelRequirements }>()
</script>
<template>
  <section class="panel" aria-labelledby="tools-title">
    <h3 id="tools-title">Tool calls</h3>
    <p class="muted">Selection records the approved plan; execution records what actually ran.</p>
    <p v-if="requirements.budget_amount != null" class="tool-budget-context"><strong>Overall trip budget:</strong> {{ formatMoney(requirements.budget_amount, requirements.currency) }} {{ requirements.budget_scope === 'PER_PERSON' ? 'per traveler' : requirements.budget_scope === 'TOTAL_TRIP' ? 'total' : '(scope not specified)' }}</p>
    <div v-if="tools.length" class="tool-grid"><ToolCallCard v-for="tool in tools" :key="tool.tool_name" :tool="tool" /></div>
    <p v-else class="empty-state">No tools selected or executed.</p>
  </section>
</template>
