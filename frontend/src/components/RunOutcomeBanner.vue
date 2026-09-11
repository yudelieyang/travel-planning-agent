<script setup lang="ts">
import type { ApiError } from '../api/travelApi.ts'
import type { PlanResponse } from '../types/travel.ts'
defineProps<{ response: PlanResponse | null; transportError: ApiError | null; submitting: boolean }>()
</script>

<template>
  <div aria-live="polite" aria-atomic="true">
    <section v-if="submitting" class="outcome running">
      <h2>Running</h2><p>Waiting for the backend’s completed execution record.</p>
    </section>
    <section v-else-if="transportError" class="outcome transport-error" role="alert">
      <h2>{{ transportError.statusCode ? `HTTP ERROR · ${transportError.statusCode}` : 'NETWORK / REQUEST ERROR' }}</h2>
      <p>{{ transportError.message }}</p>
    </section>
    <section v-else-if="response" class="outcome" :class="response.status">
      <template v-if="response.status === 'success'">
        <h2>SUCCESS · Itinerary prepared</h2><p>Review the backend’s budget comparison and estimate warnings below.</p>
      </template>
      <template v-else-if="response.status === 'needs_clarification'">
        <h2>CLARIFICATION REQUIRED</h2>
        <p>{{ response.clarification_question ?? 'Please add the missing travel details.' }}</p>
        <p v-if="response.missing_fields?.length">Missing: {{ response.missing_fields.join(', ') }}</p>
        <p class="help">Edit the full request and submit again. Each run is independent.</p>
      </template>
      <template v-else>
        <h2>DOMAIN ERROR · No validated itinerary</h2>
        <ul v-if="response.errors?.length"><li v-for="(error, i) in response.errors" :key="i">{{ error }}</li></ul>
        <p v-else>The backend could not produce a travel plan.</p>
      </template>
    </section>
  </div>
</template>
