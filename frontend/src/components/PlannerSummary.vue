<script setup lang="ts">
import type { PublicExecutionSummary } from '../types/travel.ts'
import { formatEnumLabel, yesNo } from '../utils/presentation.ts'
defineProps<{ execution: PublicExecutionSummary }>()
</script>
<template>
  <section class="panel" aria-labelledby="planner-title">
    <h3 id="planner-title">Planner</h3>
    <dl class="summary-grid">
      <div><dt>Type</dt><dd>{{ execution.planner_type }}</dd></div>
      <div><dt>Invoked</dt><dd>{{ yesNo(execution.planner_invoked) }}</dd></div>
      <div><dt>Outcome</dt><dd>{{ formatEnumLabel(execution.planner_outcome) }}</dd></div>
      <div v-if="execution.prompt_version != null"><dt>Prompt version</dt><dd>{{ execution.prompt_version }}</dd></div>
    </dl>
    <p v-if="!execution.planner_invoked && execution.stages.some(stage => stage.name === 'clarification' && stage.outcome === 'completed')" class="muted">Planner was not invoked because execution stopped at clarification.</p>
  </section>
</template>
