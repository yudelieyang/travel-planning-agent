<script setup lang="ts">
import DemoHeader from './components/DemoHeader.vue'
import TravelRequestPanel from './components/TravelRequestPanel.vue'
import RunOutcomeBanner from './components/RunOutcomeBanner.vue'
import ResultsShell from './components/ResultsShell.vue'
import DemoTakeaway from './components/DemoTakeaway.vue'
import { presets } from './presets.ts'
import { useTravelPlan } from './composables/useTravelPlan.ts'

const { draftQuery, submittedQuery, response, requestState, transportError, submit, reset } = useTravelPlan()
function loadScenario(query: string) {
  reset()
  draftQuery.value = query
}
</script>

<template>
  <main class="page">
    <DemoHeader :execution="response?.execution" />
    <TravelRequestPanel v-model="draftQuery" :submitting="requestState === 'submitting'" @select="loadScenario" @submit="submit" @reset="reset" />
    <section v-if="submittedQuery" class="submitted-request" aria-label="Submitted request">
      <strong>Submitted request</strong><p>{{ submittedQuery }}</p>
    </section>
    <RunOutcomeBanner :response="response" :transport-error="transportError" :submitting="requestState === 'submitting'" />
    <div v-if="response?.status === 'needs_clarification'" class="recovery-note">
      <p>Edit the request above and submit the full trip request again. Each run is independent.</p>
      <button type="button" @click="loadScenario(presets[0].query)">Load complete Boston example</button>
    </div>
    <DemoTakeaway :response="response" :submitted-query="submittedQuery" />
    <ResultsShell :response="response" />
    <p v-if="response" class="next-scenario"><a href="#request-panel">Try another scenario</a></p>
    <footer>Bounded English extraction · Mock travel estimates · Recorded constraints are not verified</footer>
  </main>
</template>
