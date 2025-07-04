
<template>
  <div class="bg-gray-100 min-h-screen">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Anúncios da Comunidade</h1>
      <div class="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        <AnnouncementCard v-for="announcement in announcements" :key="announcement.id" :announcement="announcement" />
      </div>
      <div class="mt-12">
        <MassMessageForm />
      </div>
      <div class="mt-12 text-center">
        <SocialLinks />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import AnnouncementCard from '~/components/AnnouncementCard.vue';
import MassMessageForm from '~/components/MassMessageForm.vue';
import SocialLinks from '~/components/SocialLinks.vue';

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
