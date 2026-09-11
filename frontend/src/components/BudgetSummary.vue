<script setup lang="ts">
import type { BudgetSummary, PublicExecutionSummary, PlanStatus } from '../types/travel.ts'
import { categoryLabels, formatBudgetScope, formatCostBasis, formatMoney, formatRemainingBudget, resultBudgetStatus } from '../utils/presentation.ts'
defineProps<{ budget?: BudgetSummary | null; status?: PlanStatus; execution?: PublicExecutionSummary | null }>()
</script>
<template>
  <section class="panel budget-panel" aria-labelledby="budget-title">
    <h3 id="budget-title">Budget summary</h3>
    <template v-if="budget">
      <p :class="['result-budget-status', { 'over-budget': budget.within_budget === false, 'within-budget': budget.within_budget === true }]">{{ resultBudgetStatus(budget) }}</p>
      <dl class="budget-metrics">
        <div><dt>{{ budget.basis === 'group' ? 'Estimated group trip cost' : 'Estimated trip cost per traveler' }}</dt><dd>{{ formatMoney(budget.estimated_total_cost, budget.currency) }}</dd></div>
        <div><dt>{{ formatBudgetScope(budget.budget_scope) }}</dt><dd>{{ budget.provided_limit == null ? 'No budget limit provided' : formatMoney(budget.provided_limit, budget.limit_currency) }}</dd></div>
        <div><dt>{{ budget.budget_scope === 'PER_PERSON' ? 'Budget balance per traveler' : 'Budget balance' }}</dt><dd :class="{ 'over-budget': budget.within_budget === false }">{{ budget.within_budget == null ? 'Comparison unavailable' : formatRemainingBudget(budget.remaining_budget, budget.limit_currency) }}</dd></div>
      </dl>
      <p v-if="budget.within_budget == null && budget.provided_limit != null" class="info-note">The available information is not sufficient for a verified budget comparison.</p>
      <dl class="summary-grid budget-context">
        <div><dt>Cost basis</dt><dd>{{ formatCostBasis(budget.basis) }}<template v-if="budget.travelers != null"> · {{ budget.travelers }} {{ budget.travelers === 1 ? 'traveler' : 'travelers' }}</template></dd></div>
        <div><dt>Estimated cost per traveler</dt><dd>{{ formatMoney(budget.per_traveler_cost, budget.currency) }}</dd></div>
        <div><dt>{{ budget.budget_scope === 'PER_PERSON' ? 'Compared cost per traveler' : budget.budget_scope === 'TOTAL_TRIP' ? 'Compared whole trip cost' : 'Compared cost' }}</dt><dd>{{ budget.comparison_cost == null ? 'Comparison unavailable' : formatMoney(budget.comparison_cost, budget.currency) }}</dd></div>
      </dl>
      <h4>Cost breakdown <span class="muted">· {{ formatCostBasis(budget.basis) }}</span></h4>
      <dl class="cost-breakdown"><div v-for="(value, category) in budget.breakdown" :key="category"><dt>{{ categoryLabels[category] }}</dt><dd>{{ formatMoney(value, budget.currency) }}</dd></div></dl>
      <p v-if="!Object.keys(budget.breakdown).length" class="muted">No category breakdown reported.</p>
    </template>
    <div v-else class="result-empty">
      <strong>No budget result</strong>
      <p v-if="status === 'needs_clarification'">Budget calculation was not reached. Complete the required trip details first.</p>
      <p v-else-if="execution?.tools.some(tool => tool.tool_name === 'calculate_budget' && !tool.executed && tool.status === 'SKIPPED')">Budget calculation was skipped.<template v-if="execution.tools.some(tool => tool.tool_name !== 'calculate_budget' && tool.executed && (tool.status === 'NO_RESULTS' || tool.status === 'ERROR'))"> Search tools returned no usable options or reported errors.</template></p>
      <p v-else>No budget summary available for this run.</p>
    </div>
  </section>
</template>
