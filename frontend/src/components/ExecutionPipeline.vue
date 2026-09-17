<script setup lang="ts">
import { computed } from 'vue'
import type { PlanStatus, PublicExecutionSummary, StageOutcome } from '../types/travel.ts'
import { formatEnumLabel } from '../utils/presentation.ts'

const props = defineProps<{ execution: PublicExecutionSummary; status: PlanStatus }>()
function observed(name: string) { return props.execution.stages.filter(stage => stage.name === name && stage.sequence != null) }
function outcome(names: string[]): StageOutcome {
  const stages = names.flatMap(observed)
  if (!stages.length) return 'not_reached'
  if (stages.some(stage => stage.outcome === 'failed')) return 'failed'
  if (stages.some(stage => stage.outcome === 'clarification')) return 'clarification'
  if (stages.every(stage => stage.outcome === 'skipped')) return 'skipped'
  return 'completed'
}
const flow = computed(() => [
  { name: 'User request', outcome: 'completed' as StageOutcome, detail: 'Natural-language trip request received.' },
  { name: 'Requirements understanding', outcome: outcome(['preflight', 'clarification']), detail: props.execution.requirement_status === 'SUFFICIENT' ? 'Required fields and semantic boundaries identified.' : 'Missing or unsafe-to-assume details surfaced.' },
  { name: 'Candidate retrieval / selection', outcome: outcome(['planner', 'tools']), detail: props.execution.planner_invoked ? 'Planner-selected tools returned controlled candidates.' : 'Stopped before candidate retrieval.' },
  { name: 'Validation', outcome: props.execution.validation.performed ? (props.execution.validation.outcome === 'passed' ? 'completed' as StageOutcome : 'failed' as StageOutcome) : outcome(['validation']), detail: props.execution.repair && props.execution.validation.outcome === 'passed' ? 'Initial validation failed; repair revalidated successfully.' : props.execution.validation.performed ? `Final validation ${props.execution.validation.outcome}.` : 'Validation was not reached.' },
  { name: 'Repair / final result', outcome: props.status === 'error' ? 'failed' as StageOutcome : props.status === 'needs_clarification' ? 'clarification' as StageOutcome : 'completed' as StageOutcome, detail: props.execution.repair ? `One bounded repair attempt; final result ${props.execution.repair.final_outcome}.` : props.status === 'needs_clarification' ? 'Safe clarification returned.' : 'Final result assembled without repair.' },
])
</script>

<template>
  <section class="panel" aria-labelledby="pipeline-title">
    <p class="stage-kicker">Five-stage decision story</p>
    <h3 id="pipeline-title">From request to validated result</h3>
    <ol class="pipeline recruiter-pipeline">
      <li v-for="(stage, index) in flow" :key="stage.name" :class="['stage', stage.outcome]">
        <span class="stage-sequence">Stage {{ index + 1 }}</span><strong>{{ stage.name }}</strong><span class="status-text">{{ formatEnumLabel(stage.outcome) }}</span><small>{{ stage.detail }}</small>
      </li>
    </ol>
  </section>
</template>
