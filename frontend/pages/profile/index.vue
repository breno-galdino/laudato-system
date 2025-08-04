<template>
  <div class="container mx-auto px-6 py-8">
    <div v-if="user" class="bg-white p-8 rounded-lg shadow-md">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">Perfil de Usuário</h1>
      <div class="flex items-center space-x-6 mb-6">
        <!--  -->
        <div>
          <h2 class="text-2xl font-semibold text-gray-700">{{ user.full_name }}</h2>
        </div>
      </div>
      <div>
        <h3 class="text-xl font-semibold text-gray-800 mb-4">Informações Adicionais</h3>
        <p class="text-gray-600"><span class="font-semibold">Nome de usuário:</span> {{ user.username }}</p>
        <p class="text-gray-600"><span class="font-semibold">Email:</span> {{ user.email }}</p>
        <p class="text-gray-600"><span class="font-semibold">Membro desde:</span> {{ new Date(user.created_at).toLocaleDateString() }}</p>
        <p class="text-gray-600"><span class="font-semibold">Última atualização:</span> {{ new Date(user.updated_at).toLocaleDateString() }}</p>
        <p class="text-gray-600 flex items-center">
          <span class="font-semibold">Status:</span>
          <span
            :class="[
              'font-bold ml-1',
              user.is_active ? 'text-green-600' : 'text-red-600'
            ]"
          >
            {{ user.is_active ? 'Ativo' : 'Inativo' }}
          </span>
        </p>
      </div>
      <div class="mt-8">
        <button @click="logout" class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700">
          Sair
        </button>
      </div>
    </div>
    <div v-else class="text-center">
      <p class="text-gray-600">Carregando perfil...</p>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/useAuthStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const user = authStore.user

if (!user) {
  router.push('/login')
}

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
/* Adicione estilos personalizados aqui, se necessário */
</style>
