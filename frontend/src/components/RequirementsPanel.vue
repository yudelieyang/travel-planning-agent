<script setup lang="ts">
import { computed } from 'vue'
import type { PublicExecutionSummary, TravelRequirements } from '../types/travel.ts'
import { formatEnumLabel, formatMoney, requirementState } from '../utils/presentation.ts'

const props = defineProps<{ requirements: TravelRequirements; missingFields: string[]; execution?: PublicExecutionSummary | null }>()
const fields: [keyof TravelRequirements, string][] = [
  ['destination', 'Destination'], ['origin', 'Origin'], ['start_date', 'Start date'], ['end_date', 'End date'],
  ['duration_days', 'Duration'], ['travelers', 'Travelers'], ['budget_amount', 'Budget'], ['budget_scope', 'Budget scope'],
]
const rows = computed(() => fields.map(([key, label]) => {
  const value = props.requirements[key]
  const state = requirementState(key, value, props.missingFields)
  const display = state === 'missing' ? 'MISSING — required' : state === 'empty' ? 'None supplied'
    : state === 'absent' ? 'Not supplied' : key === 'budget_amount' ? formatMoney(value as number, props.requirements.currency)
      : key === 'budget_scope' ? formatEnumLabel(value as string) : key === 'duration_days' ? `${value} days` : value
  return { key, label, state, display }
}))
const hardConstraints = computed(() => props.requirements.requirements_v2?.constraints ?? [])
const softPreferences = computed(() => props.requirements.requirements_v2?.preferences ?? props.requirements.specific_preferences ?? [])
const objectives = computed(() => props.requirements.requirements_v2?.objectives ?? (props.requirements.objective ? [props.requirements.objective] : []))
const ambiguities = computed(() => props.requirements.requirements_v2?.ambiguities ?? [])
const semantic = computed(() => props.execution?.semantic)
</script>

<template>
  <section class="panel" aria-labelledby="requirements-title">
    <div class="panel-heading">
      <div><p class="stage-kicker">Stage 2</p><h3 id="requirements-title">Requirements understanding</h3></div>
      <span class="badge semantic-badge">{{ (semantic?.mode ?? 'deterministic').toUpperCase() }}</span>
    </div>
    <p class="muted semantic-explainer">
      <template v-if="semantic?.mode === 'hybrid'">Hybrid mode invokes the semantic extractor only when the deterministic coverage gate finds a gap. Model output is a proposal and is quarantined until conservative merge checks pass.</template>
      <template v-else>Deterministic mode uses the bounded parser only. Coverage gaps remain visible; no semantic model is called.</template>
    </p>
    <p v-if="semantic" class="semantic-runline">
      Coverage gate: <strong>{{ semantic.coverage_triggered ? 'triggered' : 'not triggered' }}</strong>
      · Model: <strong>{{ semantic.llm_invoked ? 'invoked' : 'not invoked' }}</strong>
      · Final source: <strong>{{ formatEnumLabel(semantic.final_source) }}</strong>
      · Merge boundary: <strong>{{ semantic.requires_clarification ? 'clarification required' : 'clear' }}</strong>
      <template v-if="semantic.extractor_prompt_version"> · {{ semantic.extractor_prompt_version }}</template>
      <template v-if="semantic.extractor_model"> · {{ semantic.extractor_model }}</template>
    </p>
    <ul v-if="semantic?.coverage_reasons.length" class="tags coverage-reasons"><li v-for="reason in semantic.coverage_reasons" :key="reason">{{ formatEnumLabel(reason) }}</li></ul>

    <dl class="requirements-grid">
      <div v-for="row in rows" :key="row.key" :class="['requirement', row.state]">
        <dt>{{ row.label }}</dt><dd>{{ row.display }}</dd>
      </div>
    </dl>

    <div class="semantic-grid">
      <section>
        <h4>Hard constraints</h4>
        <ul v-if="hardConstraints.length" class="semantic-list">
          <li v-for="constraint in hardConstraints" :key="constraint.scope"><strong>{{ formatEnumLabel(constraint.scope) }} ≤ {{ formatMoney(constraint.value, constraint.currency) }}</strong><span>HARD · {{ formatEnumLabel(constraint.extractor_source ?? 'deterministic') }}</span></li>
        </ul>
        <p v-else class="muted">None extracted.</p>
      </section>
      <section>
        <h4>Soft preferences</h4>
        <ul v-if="softPreferences.length" class="semantic-list">
          <li v-for="(preference, index) in softPreferences" :key="`${preference.category}-${preference.value}-${index}`"><strong>{{ preference.value }}</strong><span>{{ formatEnumLabel(preference.category) }}</span></li>
        </ul>
        <p v-else class="muted">None extracted.</p>
      </section>
      <section>
        <h4>Objectives</h4>
        <ul v-if="objectives.length" class="semantic-list"><li v-for="objective in objectives" :key="objective"><strong>{{ formatEnumLabel(objective) }}</strong></li></ul>
        <p v-else class="muted">None extracted.</p>
      </section>
      <section :class="{ 'attention-box': ambiguities.some(item => item.level === 'BLOCKING') }">
        <h4>Unsupported / clarification-bound</h4>
        <ul v-if="ambiguities.length" class="semantic-list">
          <li v-for="(ambiguity, index) in ambiguities" :key="index"><strong>{{ formatEnumLabel(ambiguity.level) }} · {{ ambiguity.reason }}</strong><span>“{{ ambiguity.source_text }}”</span></li>
        </ul>
        <p v-else class="muted">None detected.</p>
      </section>
    </div>
    <p v-if="requirements.constraints?.length" class="info-note">Legacy notes: {{ requirements.constraints.join('; ') }}</p>
  </section>
</template>
