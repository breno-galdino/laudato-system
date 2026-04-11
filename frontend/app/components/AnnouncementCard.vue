
<template>
  <v-card>
    <v-img v-if="announcement.image" :src="announcement.image" alt="Announcement Image" height="192px" cover></v-img>
    <v-card-item>
      <v-card-title>{{ announcement.title }}</v-card-title>
      <v-card-subtitle>{{ announcement.date }}</v-card-subtitle>
    </v-card-item>
    <v-card-text>
      {{ announcement.description }}
    </v-card-text>
  </v-card>
</template>

<script setup>
const props = defineProps({
  announcement: {
    type: Object,
    required: true
  }
});
</script>
