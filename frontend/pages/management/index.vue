<template>
  <v-container>
    <n-h1 align="center" class="mb-12">Painel de Gerenciamento</n-h1>
    <v-row>
      <v-col v-for="item in managementItems" :key="item.title" cols="12" md="6">
          <v-card hover :to="item.to" class="fill-height" variant="outlined" elevation="2">
            <v-card-text>
              <div class="d-flex align-center">
                <v-avatar :color="item.color" size="56" class="mr-4">
                  <v-icon :icon="item.icon" color="white" size="large"></v-icon>
                </v-avatar>
                <div>
                  <v-card-title class="pa-0 text-h5">{{ item.title }}</v-card-title>
                  <v-card-subtitle>{{ item.description }}</v-card-subtitle>
                </div>
              </div>
            </v-card-text>
          </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';

const managementItems = ref([
  {
    title: 'Anúncios',
    description: 'Crie, edite e exclua anúncios da comunidade.',
    icon: 'mdi:mdi-bullhorn',
    to: '/management/announcements',
    color: 'blue'
  },
  {
    title: 'Comunidade',
    description: 'Gerencie os membros e as configurações da comunidade.',
    icon: 'mdi:mdi-account-group',
    to: '/management/community',
    color: 'green'
  },
  {
    title: 'Devocional',
    description: 'Administre o conteúdo devocional, como orações e velas.',
    icon: 'mdi:mdi-book-open-page-variant',
    to: '/management/devotional',
    color: 'orange'
  },
  {
    title: 'Usuários',
    description: 'Gerencie as contas e permissões dos usuários.',
    icon: 'mdi:mdi-account-cog',
    to: '/management/users',
    color: 'red'
  }
]);
</script>