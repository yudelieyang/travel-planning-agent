<script setup lang="ts">
import type { ExecutionStage } from '../types/travel.ts'
import { formatEnumLabel, stageNames } from '../utils/presentation.ts'
defineProps<{ stages: ExecutionStage[] }>()
</script>
<template>
  <section class="panel" aria-labelledby="pipeline-title">
    <h3 id="pipeline-title">Execution pipeline</h3>
    <p class="muted">Returned execution history · ordered by the backend. Unreached stages remain visible.</p>
    <ol v-if="stages.length" class="pipeline">
      <li v-for="stage in stages" :key="stage.name" :class="['stage', stage.outcome]">
        <span class="stage-sequence">{{ stage.sequence == null ? 'Unreached' : `Step ${stage.sequence}` }}</span>
        <strong>{{ stageNames[stage.name] }}</strong>
        <span class="status-text">{{ formatEnumLabel(stage.outcome) }}</span>
      </li>
    </ol>
    <p v-else class="muted">No stages reported.</p>
    <p class="muted">Finalization describes response assembly; the overall request outcome is shown above.</p>
  </section>
</template>
