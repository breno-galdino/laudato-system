<template>
  <v-container fluid class="management-container py-16">
    <!-- Título -->
    <div class="text-center mb-16">
      <h1 class="font-weight-bold text-primary text-h3 mb-2">
        Painel de Gerenciamento
      </h1>
      <p class="text-body-1 text-medium-emphasis">
        <template v-if="authStore.parish?.name">
          {{ authStore.parish.name }}
        </template>
        <template v-else>
          Escolha uma área para administrar
        </template>
      </p>
    </div>

    <!-- Cards -->
    <v-row class="justify-center" dense>
      <v-col
        v-for="item in managementItems"
        :key="item.title"
        cols="12"
        sm="6"
        md="4"
        lg="3"
        class="d-flex"
      >
        <v-hover v-slot="{ isHovering, props }">
          <v-card
            v-bind="props"
            :to="item.to"
            class="management-card fill-height"
            elevation="isHovering ? 8 : 2"
            width="100%"
          >
            <v-card-text class="d-flex flex-column align-center text-center">
              <v-avatar
                :color="item.color"
                size="72"
                class="mb-4 elevation-3"
              >
                <v-icon :icon="item.icon" size="36" color="white"></v-icon>
              </v-avatar>
              <h2 class="text-h6 font-weight-bold mb-2">{{ item.title }}</h2>
              <p class="text-body-2 text-medium-emphasis">
                {{ item.description }}
              </p>
            </v-card-text>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useAuthStore } from '~/stores/useAuthStore.js';
const authStore = useAuthStore();

const managementItems = ref([
  {
    title: 'Anúncios',
    description: 'Crie, edite e exclua anúncios da comunidade.',
    icon: 'mdi:mdi-bullhorn',
    to: '/management/announcements',
    color: 'blue-darken-2'
  },
  {
    title: 'Escalas e Missas',
    description: 'Gerencie as missas e responsáveis.',
    icon: 'mdi:mdi-calendar-check',
    to: '/management/schedules',
    color: 'purple-darken-2'
  },
  {
    title: 'Comunidade',
    description: 'Gerencie os membros e as configurações da comunidade.',
    icon: 'mdi:mdi-account-group',
    to: '/management/community',
    color: 'green-darken-2'
  },
  {
    title: 'Devocional',
    description: 'Administre o conteúdo devocional, como orações e velas.',
    icon: 'mdi:mdi-book-open-page-variant',
    to: '/management/devotional',
    color: 'orange-darken-2'
  },
  {
    title: 'Sacramentos',
    description: 'Registre e consulte batismos, crismas, matrimônios e demais sacramentos.',
    icon: 'mdi:mdi-church',
    to: '/management/sacraments',
    color: 'teal-darken-2'
  },
  {
    title: 'Usuários',
    description: 'Gerencie as contas e permissões dos usuários.',
    icon: 'mdi:mdi-account-cog',
    to: '/management/users',
    color: 'red-darken-2'
  }
]);
</script>

<style scoped>
.management-container {
  background: linear-gradient(180deg, #f9fafb 0%, #f0f2f5 100%);
  min-height: 100vh;
}

.management-card {
  border-radius: 20px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.management-card:hover {
  transform: translateY(-6px) scale(1.02);
}

h1 {
  letter-spacing: -0.5px;
}

h2 {
  color: #2c3e50;
}

p {
  line-height: 1.4;
}
</style>
