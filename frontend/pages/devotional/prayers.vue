<template>
  <v-container>
    <n-h1 align="center" class="mb-8">Orações e Novenas em Áudio</n-h1>
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <n-space vertical size="large">
          <PrayerAudioPlayer v-for="prayer in prayers" :key="prayer.id" :prayer="prayer" />
        </n-space>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import PrayerAudioPlayer from '~/components/PrayerAudioPlayer.vue';

const prayers = ref([
  { id: 1, title: 'O Santo Rosário', description: 'Uma bela recitação do Santo Rosário.', audioSrc: '' },
  { id: 2, title: 'Novena a São José', description: 'Uma novena de nove dias ao patrono da Igreja universal.', audioSrc: '' },
]);
</script>