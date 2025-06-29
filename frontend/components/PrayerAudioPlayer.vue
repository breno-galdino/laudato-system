
<template>
  <div class="bg-gray-100 p-4 rounded-lg shadow-md flex items-center">
    <div class="flex-grow">
      <h3 class="text-xl font-bold text-gray-800">{{ prayer.title }}</h3>
      <p class="text-gray-600">{{ prayer.description }}</p>
    </div>
    <audio controls :src="prayer.audioSrc" class="w-full md:w-auto mt-4 md:mt-0"></audio>
  </div>
</template>

<script setup>
const props = defineProps({
  prayer: {
    type: Object,
    required: true
  }
});
</script>
