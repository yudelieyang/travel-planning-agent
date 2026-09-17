<script setup lang="ts">
import { computed } from 'vue'
import { uniqueWarnings } from '../utils/presentation.ts'
import type { PlanResponse } from '../types/travel.ts'
import RequirementsPanel from './RequirementsPanel.vue'
import ExecutionPipeline from './ExecutionPipeline.vue'
import PlannerSummary from './PlannerSummary.vue'
import ToolCallsPanel from './ToolCallsPanel.vue'
import CandidateExplorer from './CandidateExplorer.vue'
import ValidationPanel from './ValidationPanel.vue'
import BudgetSummary from './BudgetSummary.vue'
import ItinerarySummary from './ItinerarySummary.vue'
import DiagnosticsDrawer from './DiagnosticsDrawer.vue'
const props = defineProps<{ response: PlanResponse | null }>()
const warnings = computed(() => uniqueWarnings(props.response?.warnings, props.response?.budget?.warnings, props.response?.itinerary?.warnings))
const usesSnapshots = computed(() => props.response?.execution?.tools.some(tool => tool.source === 'snapshot'))
</script>
<template>
  <section aria-labelledby="results-title">
    <div class="section-heading results-heading"><span class="section-index">02</span><h2 id="results-title">Run overview</h2></div>
    <p v-if="!response" class="empty-state">Submit a request to see the backend’s requirements, execution and results.</p>
    <div v-else class="execution-story">
      <template v-if="response.execution">
        <ExecutionPipeline :execution="response.execution" :status="response.status" />
        <RequirementsPanel :requirements="response.requirements" :missing-fields="response.missing_fields ?? []" :execution="response.execution" />
        <CandidateExplorer v-if="response.execution.candidate_groups?.length" :groups="response.execution.candidate_groups" :tools="response.execution.tools" :repair="response.execution.repair" />
        <ValidationPanel :validation="response.execution.validation" :repair="response.execution.repair" />
      </template>
      <template v-else>
        <RequirementsPanel :requirements="response.requirements" :missing-fields="response.missing_fields ?? []" />
        <p class="empty-state">No execution record available.</p>
      </template>
      <div class="trip-results">
        <BudgetSummary :budget="response.budget" :status="response.status" :execution="response.execution" />
        <p v-if="response.execution?.mode === 'demo' && (response.budget || response.itinerary)" class="muted result-disclosure">
          <template v-if="usesSnapshots">POIs come from frozen OpenStreetMap snapshots; costs are planner estimates, and transport is a synthetic allowance.</template>
          <template v-else>Controlled candidate data and costs are deterministic demo estimates.</template>
        </p>
        <ItinerarySummary :itinerary="response.itinerary" :basis="response.budget?.basis" :status="response.status" :execution="response.execution" />
      </div>
      <section v-if="warnings.length" class="panel warnings" aria-labelledby="warnings-title">
        <h3 id="warnings-title">Estimate limitations</h3><ul><li v-for="(warning, index) in warnings" :key="index">{{ warning }}</li></ul>
      </section>
      <details v-if="response.execution" class="technical-details">
        <summary>Technical execution details</summary>
        <div class="technical-details-body"><PlannerSummary :execution="response.execution" /><ToolCallsPanel :tools="response.execution.tools" :requirements="response.requirements" /></div>
      </details>
      <DiagnosticsDrawer v-if="response.execution" :execution="response.execution" />
    </div>
  </section>
</template>
