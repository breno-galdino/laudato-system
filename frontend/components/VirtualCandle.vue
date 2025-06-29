
<template>
  <div class="text-center p-4">
    <Icon name="mdi:candle" class="text-6xl text-yellow-500 animate-pulse" />
    <p class="text-gray-600 mt-2">{{ candle.intention }}</p>
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
