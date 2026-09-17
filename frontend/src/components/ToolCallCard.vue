<script setup lang="ts">
import { computed } from 'vue'
import type { PublicToolRecord } from '../types/travel.ts'
import { budgetLabel, formatEnumLabel, formatMoney, isSearchInput, quoteUnits, sameSearchInputs, toolNames, yesNo } from '../utils/presentation.ts'
const props = defineProps<{ tool: PublicToolRecord }>()
const searchInputs = computed(() => {
  const requested = props.tool.requested_arguments
  const runtime = props.tool.executed ? props.tool.runtime_arguments : null
  if (sameSearchInputs(requested, runtime) && isSearchInput(runtime)) return [{ label: 'Approved requested / runtime inputs', value: runtime }]
  return [
    ...(isSearchInput(requested) ? [{ label: 'Approved requested inputs', value: requested }] : []),
    ...(isSearchInput(runtime) ? [{ label: 'Runtime inputs', value: runtime }] : []),
  ]
})
const budgetInput = computed(() => props.tool.executed && props.tool.runtime_arguments && 'items' in props.tool.runtime_arguments ? props.tool.runtime_arguments : null)
const budgetResult = computed(() => props.tool.data && !Array.isArray(props.tool.data) ? props.tool.data : null)
const hasUnsetPriceCeiling = computed(() => searchInputs.value.some(input => input.value.max_price == null))
</script>
<template>
  <article :class="['tool-card', `tool-${tool.status.toLowerCase()}`]" :aria-label="toolNames[tool.tool_name]">
    <header class="tool-heading"><h4>{{ toolNames[tool.tool_name] }}</h4><strong class="status-text">{{ formatEnumLabel(tool.status) }}</strong></header>
    <p class="tool-state">Selected: <strong>{{ yesNo(tool.selected) }}</strong> · Executed: <strong>{{ yesNo(tool.executed) }}</strong><span v-if="tool.execution_order != null"> · Order {{ tool.execution_order }}</span></p>
    <p class="muted">Source: {{ tool.source ?? 'Not available' }}</p>
    <template v-if="tool.tool_name !== 'calculate_budget'">
      <section v-for="input in searchInputs" :key="input.label" class="tool-inputs">
        <h5>{{ input.label }}</h5>
        <dl>
          <div><dt>Destination</dt><dd>{{ input.value.destination }}</dd></div>
          <div><dt>Search price ceiling</dt><dd>{{ input.value.max_price == null ? 'Not set' : formatMoney(input.value.max_price) }}</dd></div>
          <div><dt>Preferences</dt><dd>{{ input.value.preferences?.length ? input.value.preferences.join(', ') : 'None supplied' }}</dd></div>
        </dl>
      </section>
      <p v-if="hasUnsetPriceCeiling" class="muted">Overall trip budget is enforced during itinerary budgeting and validation. Candidate prices are still compared during planning.</p>
      <p v-if="!searchInputs.length" class="muted">No input details reported.</p>
      <p v-if="!tool.executed" class="muted">Not executed — no runtime inputs.</p>
      <p v-else-if="!tool.runtime_arguments" class="muted">No runtime inputs reported.</p>
    </template>
    <template v-else>
      <section v-if="budgetInput" class="tool-inputs">
        <h5>Resolved runtime inputs</h5>
        <p class="muted">Cost inputs resolved by the backend.</p>
        <dl>
          <div><dt>Travelers</dt><dd>{{ budgetInput.travelers ?? 'Not supplied' }}</dd></div>
          <div><dt>Limit</dt><dd>{{ formatMoney(budgetInput.limit, budgetInput.limit_currency) }}</dd></div>
          <div><dt>Scope</dt><dd>{{ formatEnumLabel(budgetInput.budget_scope) }}</dd></div>
        </dl>
        <details class="cost-input-details">
          <summary>{{ budgetInput.items.length }} resolved cost items</summary>
          <dl><div v-for="(item, index) in budgetInput.items" :key="index"><dt>{{ formatEnumLabel(item.category) }}</dt><dd>{{ formatMoney(item.amount) }}</dd></div></dl>
        </details>
      </section>
      <p v-else class="muted">{{ tool.executed ? 'No runtime inputs reported.' : 'Not executed — no runtime inputs.' }}</p>
    </template>
    <section v-if="tool.executed && Array.isArray(tool.data)" class="tool-results">
      <h5>{{ tool.data.length }} results</h5>
      <ul v-if="tool.data.length" class="search-results">
        <li v-for="result in tool.data" :key="result.id"><strong>{{ result.name }}</strong><span>{{ formatMoney(result.price, result.currency) }} <small>{{ quoteUnits[result.unit] }}</small></span></li>
      </ul>
      <p v-else class="muted">No matching options returned.</p>
    </section>
    <section v-else-if="tool.executed && budgetResult" class="tool-results">
      <h5>Budget result</h5>
      <p :class="['budget-status', { 'over-budget': budgetResult.within_budget === false }]">{{ budgetLabel(budgetResult.within_budget) }}</p>
      <dl>
        <div><dt>Estimated total</dt><dd>{{ formatMoney(budgetResult.estimated_total_cost, budgetResult.currency) }}</dd></div>
        <div><dt>Comparison cost</dt><dd>{{ budgetResult.comparison_cost == null ? 'Comparison unavailable' : formatMoney(budgetResult.comparison_cost, budgetResult.currency) }}</dd></div>
        <div><dt>Provided limit</dt><dd>{{ formatMoney(budgetResult.provided_limit, budgetResult.limit_currency) }}</dd></div>
        <div><dt>Remaining budget</dt><dd>{{ budgetResult.remaining_budget == null ? 'Comparison unavailable' : formatMoney(budgetResult.remaining_budget, budgetResult.limit_currency) }}</dd></div>
      </dl>
    </section>
    <p v-else class="muted">{{ tool.executed ? 'No result data reported.' : 'No result — tool did not execute.' }}</p>
    <p v-if="tool.error_code" class="tool-error">{{ formatEnumLabel(tool.error_code) }}</p>
  </article>
</template>
