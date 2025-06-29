
<template>
  <div class="bg-white min-h-screen py-12">
    <div class="container mx-auto px-4">
      <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Orações e Novenas em Áudio</h1>
      <div class="space-y-6">
        <PrayerAudioPlayer v-for="prayer in prayers" :key="prayer.id" :prayer="prayer" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import PrayerAudioPlayer from '~/components/PrayerAudioPlayer.vue';

const prayers = ref([
  { id: 1, title: 'O Santo Rosário', description: 'Uma bela recitação do Santo Rosário.', audioSrc: '' },
  { id: 2, title: 'Novena a São José', description: 'Uma novena de nove dias ao patrono da Igreja universal.', audioSrc: '' },
]);
</script>
