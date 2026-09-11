<script setup lang="ts">
import { computed } from 'vue'
import type { PlanResponse } from '../types/travel.ts'
import { findScenario } from '../presets.ts'
import { demoTakeaway } from '../utils/demo.ts'
const props = defineProps<{ response: PlanResponse | null; submittedQuery: string }>()
const facts = computed(() => findScenario(props.submittedQuery) ? demoTakeaway(props.response) : [])
</script>
<template>
  <section v-if="facts.length" class="panel demo-takeaway" aria-labelledby="takeaway-title">
    <h2 id="takeaway-title">Demo takeaway</h2>
    <p>{{ facts.join(' ') }}</p>
  </section>
</template>
