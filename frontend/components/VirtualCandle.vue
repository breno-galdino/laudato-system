<template>
  <div class="text-center pa-4">
    <v-icon size="64" color="yellow-darken-2" class="animate-pulse">mdi-candle</v-icon>
    <p class="text-body-1 mt-2">{{ candle.intention }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  candle: {
    type: Object,
    required: true
  }
});
</script>

<style scoped>
@keyframes pulse {
  50% {
    opacity: .5;
  }
}
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>