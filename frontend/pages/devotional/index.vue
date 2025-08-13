<template>
  <v-container>
    <n-h1 align="center" class="mb-8">Devocional</n-h1>
    <v-row justify="center">
      <v-col cols="12" md="4">
        <NuxtLink to="/devotional/intentions" class="text-decoration-none">
          <v-card hover class="text-center pa-6 fill-height">
            <v-icon size="64" color="primary" class="mb-4">mdi-book-open-page-variant</v-icon>
            <v-card-title class="text-h5">Intenções de Missa</v-card-title>
            <v-card-text>Envie suas intenções para a Santa Missa.</v-card-text>
          </v-card>
        </NuxtLink>
      </v-col>
      <v-col cols="12" md="4">
        <NuxtLink to="/devotional/candles" class="text-decoration-none">
          <v-card hover class="text-center pa-6 fill-height">
            <v-icon size="64" color="primary" class="mb-4">mdi-candle</v-icon>
            <v-card-title class="text-h5">Velas Virtuais</v-card-title>
            <v-card-text>Acenda uma vela virtual com sua oração pessoal.</v-card-text>
          </v-card>
        </NuxtLink>
      </v-col>
      <v-col cols="12" md="4">
        <NuxtLink to="/devotional/prayers" class="text-decoration-none">
          <v-card hover class="text-center pa-6 fill-height">
            <v-icon size="64" color="primary" class="mb-4">mdi-headphones</v-icon>
            <v-card-title class="text-h5">Orações em Áudio</v-card-title>
            <v-card-text>Ouça orações guiadas e novenas.</v-card-text>
          </v-card>
        </NuxtLink>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
</script>