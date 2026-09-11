<script setup lang="ts">
import { computed } from 'vue'
import { presets, findScenario } from '../presets.ts'
const props = defineProps<{ modelValue: string; submitting: boolean }>()
const selectedScenario = computed(() => findScenario(props.modelValue))
const emit = defineEmits<{ 'update:modelValue': [value: string]; select: [query: string]; submit: []; reset: [] }>()
</script>

<template>
  <section id="request-panel" class="panel request-panel" aria-labelledby="request-title">
    <div class="section-heading"><span class="section-index">01</span><h2 id="request-title">Travel request</h2></div>
    <p class="muted">Choose an example or write a request in English.</p>
    <div class="presets" aria-label="Example requests">
      <button v-for="preset in presets" :key="preset.id" type="button" :disabled="submitting" :aria-label="preset.label" :aria-pressed="selectedScenario?.id === preset.id"
        @click="emit('select', preset.query)"><strong>{{ preset.label }}</strong><span>{{ preset.purpose }}</span></button>
    </div>
    <div v-if="selectedScenario" class="scenario-note"><strong>What this demonstrates · {{ selectedScenario.label }}</strong><p>{{ selectedScenario.description }}</p></div>
    <p v-else-if="modelValue" class="scenario-note"><strong>Custom Request</strong> · Submit your full request; each run is independent.</p>
    <form @submit.prevent="emit('submit')">
      <label for="travel-query">Where would you like to go?</label>
      <textarea id="travel-query" :value="modelValue" :disabled="submitting" rows="4"
        aria-describedby="query-help" placeholder="Plan a 2-day trip to Boston…"
        @input="emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)" />
      <p id="query-help" class="help">Missing details are welcome: the backend can ask for clarification. Maximum 2,000 characters.</p>
      <div class="form-actions">
        <button class="primary" type="submit" :disabled="submitting || !modelValue.trim()">
          {{ submitting ? 'Running…' : 'Plan Trip' }}
        </button>
        <button type="button" :disabled="submitting" @click="emit('reset')">Reset</button>
      </div>
    </form>
  </section>
</template>
