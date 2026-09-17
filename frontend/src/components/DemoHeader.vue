<script setup lang="ts">
import { computed } from 'vue'
import type { PublicExecutionSummary } from '../types/travel.ts'
const props = defineProps<{ execution?: PublicExecutionSummary | null }>()
const usesSnapshots = computed(() => props.execution?.tools.some(tool => tool.source === 'snapshot'))
const usesMock = computed(() => props.execution?.tools.some(tool => tool.source === 'mock'))
</script>

<template>
  <header class="page-header">
    <div>
      <p class="eyebrow">Single agent · Local portfolio demo</p>
      <h1>Travel Agent</h1>
      <p class="subtitle">Visible Agent Execution</p>
    </div>
    <div class="mode-block">
      <template v-if="execution">
        <span class="badge">{{ execution.mode.toUpperCase() }} MODE</span>
        <span class="badge semantic-badge">SEMANTIC {{ (execution.semantic?.mode ?? 'deterministic').toUpperCase() }}</span>
        <span v-if="usesSnapshots" class="badge">REAL-WORLD SNAPSHOT POIs</span>
        <span v-else-if="usesMock" class="badge neutral">CONTROLLED MOCK CANDIDATES</span>
        <span v-else class="badge neutral">CANDIDATE DATA NOT USED</span>
        <span class="mono">{{ execution.planner_type }}</span>
        <span v-if="usesSnapshots">Frozen OpenStreetMap POIs · Planner-estimated costs · Synthetic transport</span>
        <span v-else-if="usesMock">Planner {{ execution.planner_invoked ? 'invoked' : 'not invoked' }} · Controlled fixture data</span>
        <span v-else>No candidate retrieval occurred in this run.</span>
      </template>
      <template v-else>
        <span class="badge neutral">Mode unconfirmed</span>
        <span>Execution and candidate data mode will be confirmed by the backend after the first run.</span>
      </template>
    </div>
  </header>
</template>
