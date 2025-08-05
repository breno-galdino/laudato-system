<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-4xl font-bold text-center text-gray-800 mb-12">Painel de Gerenciamento</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      
      <NuxtLink to="/management/announcements" class="group block p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
        <div class="flex items-center mb-4">
          <div class="p-3 bg-blue-500 rounded-full text-white mr-4">
            <Icon name="mdi:bullhorn" class="text-2xl" />
          </div>
          <h2 class="text-2xl font-bold text-gray-800">Anúncios</h2>
        </div>
        <p class="text-gray-600">Crie, edite e exclua anúncios da comunidade.</p>
      </NuxtLink>

      <NuxtLink to="/management/community" class="group block p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
        <div class="flex items-center mb-4">
          <div class="p-3 bg-green-500 rounded-full text-white mr-4">
            <Icon name="mdi:account-group" class="text-2xl" />
          </div>
          <h2 class="text-2xl font-bold text-gray-800">Comunidade</h2>
        </div>
        <p class="text-gray-600">Gerencie os membros e as configurações da comunidade.</p>
      </NuxtLink>

      <NuxtLink to="/management/devotional" class="group block p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
        <div class="flex items-center mb-4">
          <div class="p-3 bg-yellow-500 rounded-full text-white mr-4">
            <Icon name="mdi:book-open-page-variant" class="text-2xl" />
          </div>
          <h2 class="text-2xl font-bold text-gray-800">Devocional</h2>
        </div>
        <p class="text-gray-600">Administre o conteúdo devocional, como orações e velas.</p>
      </NuxtLink>

      <NuxtLink to="/management/users" class="group block p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
        <div class="flex items-center mb-4">
          <div class="p-3 bg-red-500 rounded-full text-white mr-4">
            <Icon name="mdi:account-cog" class="text-2xl" />
          </div>
          <h2 class="text-2xl font-bold text-gray-800">Usuários</h2>
        </div>
        <p class="text-gray-600">Gerencie as contas e permissões dos usuários.</p>
      </NuxtLink>

    </div>
  </div>
</template>

<script setup>
</script>
