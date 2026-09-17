<script setup lang="ts">
import { computed } from 'vue'
import type { CandidateGroup, Category, PublicToolRecord, RepairSummary, SearchToolName, TravelOption } from '../types/travel.ts'
import { formatEnumLabel, formatMoney, isSearchInput, quoteUnits } from '../utils/presentation.ts'

const props = withDefaults(defineProps<{ groups: CandidateGroup[]; tools?: PublicToolRecord[]; repair?: RepairSummary | null }>(), { tools: () => [] })
const hasOpenStreetMap = computed(() => props.groups.some(group => candidates(group).some(item => item.option.provider === 'openstreetmap')))
const toolForCategory: Record<Category, SearchToolName> = {
  attractions: 'search_attractions', hotel: 'search_hotels', food: 'search_restaurants', transport: 'search_transport',
}
function candidates(group: CandidateGroup) {
  return [...group.selected.map(option => ({ option, selected: true })), ...group.alternatives.map(option => ({ option, selected: false }))]
}
function rating(option: TravelOption) {
  if (option.rating == null) return ''
  return option.review_count == null ? `${option.rating.toFixed(1)} rating` : `${option.rating.toFixed(1)} · ${option.review_count.toLocaleString()} demo reviews`
}
function source(option: TravelOption) {
  if (option.provider === 'openstreetmap') return `OpenStreetMap snapshot${option.snapshot_version ? ` · ${option.snapshot_version}` : ''}`
  return option.source === 'controlled_mock_fixture' ? 'Controlled mock fixture' : 'Not supplied'
}
function quoteUnit(option: TravelOption) {
  if (option.provider === 'openstreetmap' && option.category === 'attractions') return 'per traveler / visit'
  if (option.provider === 'openstreetmap' && option.category === 'hotel') return 'per traveler / night'
  if (option.provider === 'openstreetmap' && option.category === 'food') return 'per traveler / meal'
  return quoteUnits[option.unit]
}
function providerCuisines(option: TravelOption) {
  return [...new Set((option.provider_category_ids ?? [])
    .filter(value => value.startsWith('cuisine='))
    .flatMap(value => value.slice('cuisine='.length).split(';'))
    .map(value => value.trim().replaceAll('_', ' '))
    .filter(Boolean))]
}
function searchRecord(category: Category) { return props.tools.find(tool => tool.tool_name === toolForCategory[category]) }
function groupSource(group: CandidateGroup) {
  if (candidates(group).some(item => item.option.provider === 'openstreetmap')) return 'Real-world OpenStreetMap snapshot · frozen, not live'
  if (group.category === 'transport') return 'Synthetic planning allowance'
  return 'Controlled mock fixture'
}
function filterText(group: CandidateGroup) {
  const input = searchRecord(group.category)?.runtime_arguments ?? null
  if (!isSearchInput(input)) return 'No runtime filter evidence available.'
  const parts = [input.max_price == null ? 'no category price ceiling' : `price ≤ ${formatMoney(input.max_price)}`]
  if (input.preferences?.length) parts.push(`preferences: ${input.preferences.join(', ')}`)
  return `${group.selected.length + group.alternatives.length} eligible candidates returned after ${parts.join(' · ')}.`
}
function why(option: TravelOption, selected: boolean) {
  if (!selected) return 'Eligible alternative retained for comparison.'
  const repaired = props.repair?.changes.some(change => change.after.some(name => name === option.name || name.startsWith(`${option.name} (`)))
  if (repaired) return 'Selected during the single bounded repair to lower cost.'
  if (option.preference_matches?.length) return `Selected with explicit preference match: ${option.preference_matches.join(', ')}.`
  return 'Selected from eligible candidates by the planner.'
}
</script>

<template>
  <section class="panel" aria-labelledby="candidate-explorer-title">
    <p class="stage-kicker">Stage 3</p><h3 id="candidate-explorer-title">Candidate retrieval and selection</h3>
    <p class="muted">Counts describe the eligible results returned by the controlled search. The source total before filtering is not exposed, so the UI does not invent a filtered-out count.</p>
    <p v-if="hasOpenStreetMap" class="muted">© OpenStreetMap contributors · OpenStreetMap data is available under the ODbL.</p>
    <div class="candidate-groups">
      <section v-for="group in groups" :key="group.category" class="candidate-group">
        <div class="candidate-group-heading"><h4>{{ formatEnumLabel(group.category) }}</h4><span>{{ groupSource(group) }} · {{ group.selected.length }} selected · {{ group.alternatives.length }} alternatives</span></div>
        <p class="filter-evidence">{{ filterText(group) }}</p>
        <div class="candidate-grid">
          <article v-for="item in candidates(group)" :key="item.option.id" :class="['candidate-card', { selected: item.selected }]">
            <img v-if="item.option.image_url" :src="item.option.image_url" alt="" loading="lazy">
            <div class="candidate-heading"><strong>{{ item.option.name }}</strong><span v-if="item.selected" class="badge">Selected</span><span v-else class="badge neutral">Alternative</span></div>
            <p v-if="item.option.address" class="muted"><strong>Address:</strong> {{ item.option.address }}</p>
            <p v-if="providerCuisines(item.option).length" class="muted"><strong>Cuisine:</strong> {{ providerCuisines(item.option).join(', ') }}</p>
            <p class="candidate-price"><span v-if="item.option.cost_origin === 'planner_estimate'">Planner estimate: </span>{{ formatMoney(item.option.price, item.option.currency) }} <small>{{ quoteUnit(item.option) }}</small></p>
            <p v-if="item.option.rating != null" class="muted">{{ rating(item.option) }}</p>
            <p v-if="item.option.provider === 'openstreetmap' && item.option.tags.length" class="muted"><strong>Planner preference tags:</strong></p>
            <ul v-if="item.option.tags.length" class="tags"><li v-for="tag in item.option.tags" :key="tag">{{ tag }}</li></ul>
            <p class="selection-reason"><strong>Why:</strong> {{ why(item.option, item.selected) }}</p>
            <p class="muted">Source: {{ source(item.option) }}</p>
          </article>
        </div>
      </section>
    </div>
  </section>
</template>
