<template>
  <v-container>
    <n-h1 align="center" class="mb-8">Anúncios da Comunidade</n-h1>
    <v-row>
      <v-col v-for="announcement in announcements" :key="announcement.id" cols="12" md="6" lg="4">
        <AnnouncementCard :announcement="announcement" />
      </v-col>
    </v-row>
    <v-row justify="center" class="mt-12">
      <v-col cols="12" md="8" lg="6">
        <MassMessageForm />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>

const announcements = ref([
  {
    id: 1,
    title: 'Festa do Padroeiro',
    description: 'Junte-se a nós para uma missa especial e celebração do dia do nosso padroeiro.',
    date: '2024-07-15',
    image: '/diocese.png'
  },
  {
    id: 2,
    title: 'Chamada para Voluntários',
    description: 'Estamos procurando voluntários para ajudar na próxima campanha de caridade.',
    date: '2024-07-12',
    image: '/logo.png'
  },
  {
    id: 3,
    title: 'Inscrições para a Catequese Abertas',
    description: 'As inscrições para o novo ano da catequese já estão abertas para todas as idades.',
    date: '2024-07-10',
    image: '/diocese.png'
  }
]);
</script>