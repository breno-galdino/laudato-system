
<template>
  <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow">
    <img v-if="announcement.image" :src="announcement.image" alt="Announcement Image" class="w-full h-48 object-cover">
    <div class="p-6">
      <h3 class="text-xl font-bold text-gray-800 mb-2">{{ announcement.title }}</h3>
      <p class="text-gray-600 mb-4">{{ announcement.description }}</p>
      <p class="text-sm text-gray-500">{{ announcement.date }}</p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  announcement: {
    type: Object,
    required: true
  }
});
</script>
