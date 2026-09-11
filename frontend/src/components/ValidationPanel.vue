<script setup lang="ts">
import type { ValidationSummary } from '../types/travel.ts'
import { formatEnumLabel, validationReasons, yesNo } from '../utils/presentation.ts'
defineProps<{ validation: ValidationSummary }>()
</script>
<template>
  <section class="panel" aria-labelledby="validation-title">
    <h3 id="validation-title">Validation</h3>
    <dl class="summary-grid">
      <div><dt>Performed</dt><dd>{{ yesNo(validation.performed) }}</dd></div>
      <div><dt>Outcome</dt><dd :class="['validation-outcome', validation.outcome]">{{ formatEnumLabel(validation.outcome) }}</dd></div>
      <div v-if="validation.reason"><dt>Reason</dt><dd>{{ validationReasons[validation.reason] }}</dd></div>
    </dl>
  </section>
</template>
