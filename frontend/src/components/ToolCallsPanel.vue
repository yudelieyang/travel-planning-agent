<script setup lang="ts">
import type { PublicToolRecord } from '../types/travel.ts'
import ToolCallCard from './ToolCallCard.vue'
defineProps<{ tools: PublicToolRecord[] }>()
</script>
<template>
  <section class="panel" aria-labelledby="tools-title">
    <h3 id="tools-title">Tool calls</h3>
    <p class="muted">Selection records the approved plan; execution records what actually ran.</p>
    <div v-if="tools.length" class="tool-grid"><ToolCallCard v-for="tool in tools" :key="tool.tool_name" :tool="tool" /></div>
    <p v-else class="empty-state">No tools selected or executed.</p>
  </section>
</template>
