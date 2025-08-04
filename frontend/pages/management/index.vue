
<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Painel de Gerenciamento</h1>
    <div class="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
      <NuxtLink to="/management/announcements" class="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
        <h2 class="text-2xl font-bold text-gray-800 mb-2">Gerenciar Anúncios</h2>
        <p class="text-gray-600">Crie, edite e exclua anúncios da comunidade.</p>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
</script>
