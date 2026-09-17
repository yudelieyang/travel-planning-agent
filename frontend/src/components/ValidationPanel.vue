<script setup lang="ts">
import type { RepairSummary, ValidationSummary } from '../types/travel.ts'
import { formatEnumLabel, formatMoney, validationReasons, yesNo } from '../utils/presentation.ts'
defineProps<{ validation: ValidationSummary; repair?: RepairSummary | null }>()
function compactNames(names: string[]) {
  return [...new Set(names.map(name => name.replace(/ \((?:breakfast|lunch|dinner)\)$/, '')))].join(', ') || 'No final selection'
}
</script>
<template>
  <section class="panel" aria-labelledby="validation-title">
    <p class="stage-kicker">Stages 4–5</p><h3 id="validation-title">Validation, bounded repair, and final result</h3>
    <dl class="summary-grid">
      <div><dt>Validation performed</dt><dd>{{ yesNo(validation.performed) }}</dd></div>
      <div><dt>Final outcome</dt><dd :class="['validation-outcome', validation.outcome]">{{ formatEnumLabel(validation.outcome) }}</dd></div>
      <div v-if="validation.reason"><dt>Reason</dt><dd>{{ validationReasons[validation.reason] }}</dd></div>
    </dl>
    <ul v-if="validation.violations?.length" class="violation-list">
      <li v-for="violation in validation.violations" :key="violation.code"><strong>{{ formatEnumLabel(violation.code) }}</strong><span>Limit {{ formatMoney(violation.expected, 'USD') }} · actual {{ formatMoney(violation.actual, 'USD') }} · exceeded by {{ formatMoney(violation.excess, 'USD') }}</span><small>{{ violation.message }}</small></li>
    </ul>
    <section v-if="repair" class="repair-story" aria-label="Bounded repair evidence">
      <div class="repair-heading"><h4>Repair attempt {{ repair.attempt }} of {{ repair.maximum_attempts }}</h4><span :class="['badge', repair.final_outcome === 'failed' && 'danger-badge']">{{ repair.final_outcome.toUpperCase() }}</span></div>
      <p><strong>Trigger:</strong> {{ repair.trigger.map(item => formatEnumLabel(item.code)).join(', ') }}. Initial total {{ formatMoney(repair.initial_total, 'USD') }}.</p>
      <p><strong>Correction:</strong> the planner received typed violation feedback and selected lower-cost eligible options once.</p>
      <p><strong>Result:</strong> {{ repair.final_total == null ? 'No final total available.' : `${formatMoney(repair.final_total, 'USD')} · ${formatMoney(repair.savings, 'USD')} saved · revalidation ${repair.final_outcome}.` }}</p>
      <ul v-if="repair.changes.length" class="repair-changes"><li v-for="change in repair.changes" :key="change.category"><strong>{{ formatEnumLabel(change.category) }}</strong><span>{{ compactNames(change.before) }} → {{ compactNames(change.after) }}</span></li></ul>
      <p class="muted">Retry policy: maximum one repair attempt; no infinite loop.</p>
    </section>
    <p v-else class="muted no-repair">Repair attempt: none. The final result required no bounded retry.</p>
  </section>
</template>
