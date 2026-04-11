<template>
  <v-container>
    <v-card v-if="user" class="pa-4">
      <v-card-title class="text-h4">Perfil de Usuário</v-card-title>
      <v-card-text>
        <div class="d-flex align-center mb-6">
          <div>
            <h2 class="text-h5">{{ user.full_name }}</h2>
          </div>
        </div>
        <div>
          <h3 class="text-h6 mb-4">Informações Adicionais</h3>
          <p><span class="font-weight-bold">Nome de usuário:</span> {{ user.username }}</p>
          <p><span class="font-weight-bold">Email:</span> {{ user.email }}</p>
          <p><span class="font-weight-bold">Membro desde:</span> {{ new Date(user.created_at).toLocaleDateString() }}</p>
          <p><span class="font-weight-bold">Última atualização:</span> {{ new Date(user.updated_at).toLocaleDateString() }}</p>
          <div class="d-flex align-center">
            <span class="font-weight-bold mr-2">Status:</span>
            <v-chip :color="user.is_active ? 'success' : 'error'" label>
              {{ user.is_active ? 'Ativo' : 'Inativo' }}
            </v-chip>
          </div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" @click="logout">Sair</v-btn>
      </v-card-actions>
    </v-card>
    <div v-else class="text-center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <p class="mt-4">Carregando perfil...</p>
    </div>
  </v-container>
</template>

<script setup>
import { useAuthStore } from '~/stores/useAuthStore.js';
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