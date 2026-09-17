<script setup lang="ts">
import type { PublicExecutionSummary } from '../types/travel.ts'
import { formatEnumLabel } from '../utils/presentation.ts'
defineProps<{ execution: PublicExecutionSummary }>()
</script>
<template>
  <details class="panel diagnostics">
    <summary>Engineering diagnostics</summary>
    <dl>
      <div><dt>Run ID</dt><dd class="mono">{{ execution.run_id }}</dd></div>
      <div><dt>Mode</dt><dd>{{ formatEnumLabel(execution.mode) }}</dd></div>
      <div><dt>Planner type</dt><dd>{{ execution.planner_type }}</dd></div>
      <div><dt>Prompt version</dt><dd>{{ execution.prompt_version ?? 'Not applicable' }}</dd></div>
      <div><dt>Latency</dt><dd>{{ execution.latency_ms }} ms</dd></div>
      <div><dt>Requirement status</dt><dd>{{ formatEnumLabel(execution.requirement_status) }}</dd></div>
      <div><dt>Planner outcome</dt><dd>{{ formatEnumLabel(execution.planner_outcome) }}</dd></div>
      <div><dt>Semantic mode</dt><dd>{{ formatEnumLabel(execution.semantic?.mode ?? 'deterministic') }}</dd></div>
      <div><dt>Semantic extraction</dt><dd>{{ formatEnumLabel(execution.semantic?.extraction_status ?? 'not_requested') }}</dd></div>
      <div><dt>Bounded repair attempts</dt><dd>{{ execution.replan_attempts ?? 0 }} / 1 maximum</dd></div>
    </dl>
  </details>
</template>
