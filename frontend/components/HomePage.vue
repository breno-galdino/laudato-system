
<template>
  <div>
    <!-- Hero Section -->
    <v-img
      v-if="!authStore?.user"
      src="/igreja.jpg"
      height="calc(100vh - 64px)"
      contain
      gradient="to right, rgba(44, 62, 80, 0.8), rgba(0, 0, 0, 0.6)"
      class="d-flex align-center text-center pa-4"
    >
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="10" lg="8">
            <h1 class="text-h2 font-weight-bold text-white mb-4">Plataforma de Gestão Paroquial Católica</h1>
            <p class="text-h5 font-weight-light text-white opacit-80 mb-8">
              Uma solução unificada para administração simplificada e engajamento comunitário vibrante.
            </p>
            <div class="d-flex justify-center ga-4">
              <v-btn size="x-large" rounded="pill" variant="outlined" color="white" href="#features">
                Saiba Mais
              </v-btn>
              <v-btn size="x-large" rounded="pill" color="primary" to="/login">
                Acessar Sistema
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-img>

    <!-- Important Notices Section -->
    <v-container class="py-16">
      <h2 class="text-h3 font-weight-bold text-center text-primary mb-12">Avisos Importantes</h2>
      <v-card class="mx-auto pa-4" max-width="900" variant="tonal">
        <v-card-item>
          <v-card-title class="text-h5">Campanha do Agasalho 2025</v-card-title>
        </v-card-item>
        <v-card-text class="text-body-1">
          Estamos arrecadando agasalhos e cobertores para ajudar as famílias necessitadas da nossa comunidade. As doações podem ser entregues na secretaria paroquial até o dia 30 de Julho.
        </v-card-text>
        <v-divider class="my-4"></v-divider>
        <v-card-item>
          <v-card-title class="text-h5">Inscrições para Catequese</v-card-title>
        </v-card-item>
        <v-card-text class="text-body-1">
          As inscrições para a catequese de 2025 estão abertas! Procure a secretaria paroquial para mais informações e para realizar a inscrição de seus filhos.
        </v-card-text>
      </v-card>
    </v-container>

    <v-divider :thickness="3"></v-divider>

    <!-- Masses and Events Section -->
    <v-container class="py-16">
      <h2 class="text-h3 font-weight-bold text-center text-primary mb-12">Calendário Paroquial</h2>
      <v-row justify="center" class="ga-8">
        <v-col cols="12" md="5">
          <h3 class="text-h4 font-weight-medium text-center mb-8">Próximas Missas</h3>
          <v-timeline side="end" align="start">
            <v-timeline-item dot-color="primary" size="small">
              <div class="d-flex">
                <strong class="me-4">09:00</strong>
                <div>
                  <strong>Missa Dominical</strong>
                  <div class="text-caption">Igreja Matriz</div>
                  <div class="text-caption mb-2">Celebrante: Pe. João Silva</div>
                </div>
              </div>
            </v-timeline-item>
            <v-timeline-item dot-color="secondary" size="small">
              <div class="d-flex">
                <strong class="me-4">18:00</strong>
                <div>
                  <strong>Missa da Família</strong>
                  <div class="text-caption">Capela São José</div>
                  <div class="text-caption mb-2">Celebrante: Pe. Pedro Santos</div>
                </div>
              </div>
            </v-timeline-item>
            <v-timeline-item dot-color="primary" size="small">
              <div class="d-flex">
                <strong class="me-4">19:30</strong>
                <div>
                  <strong>Missa Semanal</strong>
                  <div class="text-caption">Igreja Matriz</div>
                  <div class="text-caption mb-2">Celebrante: Pe. Antônio Costa</div>
                </div>
              </div>
            </v-timeline-item>
          </v-timeline>
        </v-col>

        <v-divider vertical inset class="hidden-sm-and-down"></v-divider>

        <v-col cols="12" md="5">
          <h3 class="text-h4 font-weight-medium text-center mb-8">Eventos da Paróquia</h3>
          <v-sheet elevation="2" rounded="lg">
            <v-list lines="two" density="compact">
              <v-list-item title="Festa Junina Paroquial" subtitle="20 de Julho de 2025 - Salão Paroquial"></v-list-item>
              <v-divider></v-divider>
              <v-list-item title="Retiro Espiritual Anual" subtitle="15 a 17 de Agosto de 2025 - Casa de Retiros Bom Pastor"></v-list-item>
            </v-list>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>

    <!-- Modules Section -->
    <div class="bg-grey-lighten-4 py-16">
      <v-container id="features">
        <h2 class="text-h3 font-weight-bold text-center text-primary mb-12">Módulos Principais</h2>
        <v-row>
          <v-col v-for="module in modules" :key="module.title" cols="12" sm="6" lg="4">
            <NuxtLink :to="module.path || '#'" class="text-decoration-none">
              <v-card hover class="fill-height pa-2">
                <v-card-item>
                  <template #prepend>
                    <v-icon :icon="module.icon" size="x-large" color="primary"></v-icon>
                  </template>
                  <v-card-title class="text-h6 font-weight-bold">{{ module.title }}</v-card-title>
                </v-card-item>
                <v-card-text class="text-body-1">
                  {{ module.description }}
                </v-card-text>
              </v-card>
            </NuxtLink>
          </v-col>
        </v-row>
      </v-container>
    </div>

    <!-- Special Emphasis Section -->
    <v-container class="py-16">
      <v-row align="center" justify="center" class="ga-12">
        <v-col cols="12" md="6">
          <h2 class="text-h3 font-weight-bold text-primary">Nutrindo a Fé e a Comunidade</h2>
          <p class="text-h6 font-weight-light my-6">
            Nossa plataforma foi projetada para fortalecer os laços de sua comunidade paroquial e fornecer ferramentas para o crescimento espiritual na era digital.
          </p>
          <v-list lines="two" class="bg-transparent">
            <v-list-item prepend-icon="mdi-message-text" title="Comunicação Comunitária" subtitle="Mantenha seus paroquianos informados e engajados com nossas ferramentas de comunicação integradas."></v-list-item>
            <v-list-item prepend-icon="mdi-candle" title="Ferramentas Devocionais" subtitle="Promova uma vida de oração com intenções de missa online, velas virtuais e uma biblioteca de novenas e orações."></v-list-item>
          </v-list>
        </v-col>
        <v-col cols="12" md="5" class="text-center">
          <v-img src="/logo.png" alt="Laudato System Logo" width="80%" class="mx-auto rounded-xl elevation-6" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/useAuthStore';
const authStore = useAuthStore();
const modules = ref([
  {
    title: 'Agendamento de Missas e Liturgia',
    description: 'Gerencie celebrações, designe leitores, ministros, músicos e envie lembretes automáticos.',
    icon: 'mdi-calendar-clock',
  },
  {
    title: 'Gestão de Usuários e Permissões',
    description: 'Cadastre paroquianos, atribua funções, login seguro via e-mail, CPF ou ID de membro.',
    icon: 'mdi-account-group',
  },
  {
    title: 'Eventos e Agenda Paroquial',
    description: 'Calendário completo com eventos, reuniões e horários de missas; reserva de espaços e notificações.',
    icon: 'mdi-calendar-multiselect',
  },
  {
    title: 'Biblioteca de Documentos e Conteúdo',
    description: 'Carregue e organize documentos da igreja; PDFs de catecismo, vídeos e artigos.',
    icon: 'mdi-file-document-multiple',
  },
  {
    title: 'Módulo Financeiro e de Doações',
    description: 'Gerencie dízimos, campanhas de arrecadação, gere relatórios e suporte doações online.',
    icon: 'mdi-cash-multiple',
  },
  {
    title: 'Catequese e Formação Cristã',
    description: 'Gerencie turmas, catequistas, controle de frequência e geração automática de certificados em PDF.',
    icon: 'mdi-school',
  },
  {
    title: 'Comunicação Comunitária',
    description: 'Mural de notícias, mensagens em massa via WhatsApp/e-mail e integração com redes sociais.',
    icon: 'mdi-message-text',
    path: '/community'
  },
  {
    title: 'Gestão de Pastorais e Movimentos',
    description: 'Cadastre grupos pastorais, agende reuniões e gerencie participantes.',
    icon: 'mdi-human-handsup',
  },
  {
    title: 'Módulo Devocional',
    description: 'Intenções de missa online, velas virtuais com intenções e áudio para novenas/orações.',
    icon: 'mdi-candle',
    path: '/devotional'
  },
]);

const { data: warnings } = useApi('/warnings/')

</script>
