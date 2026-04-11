<template>
  <v-card class="d-flex flex-column flex-md-row align-center pa-4">
    <div class="flex-grow-1">
      <v-card-title class="text-h5">{{ prayer.title }}</v-card-title>
      <v-card-subtitle>{{ prayer.description }}</v-card-subtitle>
    </div>
    <audio controls :src="prayer.audioSrc" class="mt-4 mt-md-0"></audio>
  </v-card>
</template>

<script setup>
const props = defineProps({
  prayer: {
    type: Object,
    required: true
  }
});
</script>