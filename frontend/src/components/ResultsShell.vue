<script setup lang="ts">
import { computed } from 'vue'
import { uniqueWarnings } from '../utils/presentation.ts'
import type { PlanResponse } from '../types/travel.ts'
import RequirementsPanel from './RequirementsPanel.vue'
import ExecutionPipeline from './ExecutionPipeline.vue'
import PlannerSummary from './PlannerSummary.vue'
import ToolCallsPanel from './ToolCallsPanel.vue'
import ValidationPanel from './ValidationPanel.vue'
import BudgetSummary from './BudgetSummary.vue'
import ItinerarySummary from './ItinerarySummary.vue'
import DiagnosticsDrawer from './DiagnosticsDrawer.vue'
const props = defineProps<{ response: PlanResponse | null }>()
const warnings = computed(() => uniqueWarnings(props.response?.warnings, props.response?.budget?.warnings, props.response?.itinerary?.warnings))
</script>
<template>
  <section aria-labelledby="results-title">
    <div class="section-heading results-heading"><span class="section-index">02</span><h2 id="results-title">Run overview</h2></div>
    <p v-if="!response" class="empty-state">Submit a request to see the backend’s requirements, execution and results.</p>
    <div v-else class="execution-story">
      <RequirementsPanel :requirements="response.requirements" :missing-fields="response.missing_fields ?? []" />
      <template v-if="response.execution">
        <ExecutionPipeline :stages="response.execution.stages" />
        <PlannerSummary :execution="response.execution" />
        <ToolCallsPanel :tools="response.execution.tools" />
        <ValidationPanel :validation="response.execution.validation" />
      </template>
      <p v-else class="empty-state">No execution record available.</p>
      <div class="trip-results">
        <BudgetSummary :budget="response.budget" :status="response.status" :execution="response.execution" />
        <p v-if="response.execution?.mode === 'demo' && (response.budget || response.itinerary)" class="muted result-disclosure">Demo travel options and costs are mock estimates.</p>
        <ItinerarySummary :itinerary="response.itinerary" :basis="response.budget?.basis" :status="response.status" :execution="response.execution" />
      </div>
      <section v-if="warnings.length" class="panel warnings" aria-labelledby="warnings-title">
        <h3 id="warnings-title">Estimate limitations</h3><ul><li v-for="(warning, index) in warnings" :key="index">{{ warning }}</li></ul>
      </section>
      <DiagnosticsDrawer v-if="response.execution" :execution="response.execution" />
    </div>
  </section>
</template>
