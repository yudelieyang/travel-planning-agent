<script setup lang="ts">
import type { PublicExecutionSummary } from '../types/travel.ts'
defineProps<{ execution?: PublicExecutionSummary | null }>()
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
        <span class="mono">{{ execution.planner_type }}</span>
        <span>Planner {{ execution.planner_invoked ? 'invoked' : 'not invoked' }} · Mock travel data</span>
      </template>
      <template v-else>
        <span class="badge neutral">Mode unconfirmed</span>
        <span>Execution mode will be confirmed by the backend.</span>
      </template>
    </div>
  </header>
</template>
