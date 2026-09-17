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
    <h3>Try a demo scenario</h3>
    <p class="muted">These optional shortcuts highlight specific agent behaviors. You can also write your own request below.</p>
    <div class="presets" aria-label="Demo scenario shortcuts">
      <button v-for="preset in presets" :key="preset.id" type="button" :disabled="submitting" :aria-label="`${preset.label}: ${preset.context}`" :aria-pressed="selectedScenario?.id === preset.id"
        @click="emit('select', preset.query)"><strong>{{ preset.label }}</strong><span class="scenario-context">{{ preset.context }}</span><span>{{ preset.purpose }}</span></button>
    </div>
    <div v-if="selectedScenario" class="scenario-note"><strong>What this demonstrates · {{ selectedScenario.label }}</strong><p>{{ selectedScenario.description }}</p></div>
    <p v-else-if="modelValue" class="scenario-note"><strong>Custom Request</strong> · Submit your full request; each run is independent.</p>
    <aside id="request-guidance" class="request-guidance" aria-labelledby="request-guidance-title">
      <h3 id="request-guidance-title">Tips for a better request</h3>
      <p>Include any details you care about: destination, duration or dates, travelers, total budget, interests, food, hotel, or transport preferences.</p>
      <p><strong>Recommended first run:</strong> use Real Snapshot Trip, then Bounded Budget Repair or Preference Matching. None needs an API key.</p>
      <p><strong>Optional live:</strong> the ambiguity, correction, and tradeoff presets require the backend’s hybrid semantic mode and an OpenAI key.</p>
      <p><strong>Clear budget wording:</strong> try “total budget of $1300,” “under $1300 total,” or “around $1300.”</p>
      <p>Optional details can be omitted. The agent may ask for clarification when required information is missing.</p>
    </aside>
    <form @submit.prevent="emit('submit')">
      <label for="travel-query">Where would you like to go?</label>
      <textarea id="travel-query" :value="modelValue" :disabled="submitting" rows="4"
        aria-describedby="request-guidance query-help" placeholder="Plan a 3-day trip to Columbus for 1 traveler under $900 total. I like zoos and fried chicken."
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
