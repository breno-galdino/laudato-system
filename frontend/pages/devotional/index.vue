
<template>
  <div class="bg-white min-h-screen">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Devocional</h1>
      <div class="grid gap-8 md:grid-cols-3">
        <NuxtLink to="/devotional/intentions" class="bg-gray-100 p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow text-center">
          <Icon name="mdi:book-open-page-variant" class="text-5xl text-yellow-600 mx-auto mb-4" />
          <h2 class="text-2xl font-bold text-gray-800">Intenções de Missa</h2>
          <p class="text-gray-600">Envie suas intenções para a Santa Missa.</p>
        </NuxtLink>
        <NuxtLink to="/devotional/candles" class="bg-gray-100 p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow text-center">
          <Icon name="mdi:candle" class="text-5xl text-yellow-600 mx-auto mb-4" />
          <h2 class="text-2xl font-bold text-gray-800">Velas Virtuais</h2>
          <p class="text-gray-600">Acenda uma vela virtual com sua oração pessoal.</p>
        </NuxtLink>
        <NuxtLink to="/devotional/prayers" class="bg-gray-100 p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow text-center">
          <Icon name="mdi:headphones" class="text-5xl text-yellow-600 mx-auto mb-4" />
          <h2 class="text-2xl font-bold text-gray-800">Orações em Áudio</h2>
          <p class="text-gray-600">Ouça orações guiadas e novenas.</p>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>
