
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
    <div class="bg-blue-grey-lighten-5 pb-16">
      <v-container>
        <h2 class="text-h3 font-weight-bold text-center text-grey-darken-3 mb-12">Avisos</h2>
        <v-row justify="center">
          <v-col v-for="(notice, i) in notices" :key="i" cols="12" md="5">
            <v-card class="fill-height" elevation="2" rounded="lg">
              <v-card-item :prepend-icon="notice.icon" :class="`bg-${notice.color}`">
                <v-card-title class="text-white font-weight-bold">{{ notice.title }}</v-card-title>
              </v-card-item>
              <v-card-text class="pa-6 text-body-1">
                {{ notice.text }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>

    <v-divider :thickness="3"></v-divider>

    <!-- Masses and Events Section -->
    <v-container class="py-16">
      <h2 class="text-h3 font-weight-bold text-center text-primary mb-12">Calendário Paroquial</h2>
      <v-row justify="center" class="ga-8">
        <v-col cols="12" md="5">
          <v-card elevation="4" rounded="lg">
            <v-card-item class="bg-primary">
              <v-card-title class="text-center text-h4 font-weight-medium">Próximas Missas</v-card-title>
            </v-card-item>
            <v-card-text>
              <v-timeline side="end" align="center" truncate-line="both" density="compact" class="py-6 px-2">
                <v-timeline-item dot-color="primary" size="small" fill-dot>
                  <v-card variant="tonal" color="primary" width="320px">
                    <v-card-title class="text-subtitle-1">09:00 - Missa Dominical</v-card-title>
                    <v-card-text class="text-caption">
                      <div>Igreja Matriz</div>
                      <div>Celebrante: Pe. João Silva</div>
                    </v-card-text>
                  </v-card>
                </v-timeline-item>
                <v-timeline-item dot-color="secondary" size="small" fill-dot>
                   <v-card variant="tonal" color="secondary" width="320px">
                    <v-card-title class="text-subtitle-1">18:00 - Missa da Família</v-card-title>
                    <v-card-text class="text-caption">
                      <div>Capela São José</div>
                      <div>Celebrante: Pe. Pedro Santos</div>
                    </v-card-text>
                  </v-card>
                </v-timeline-item>
                <v-timeline-item dot-color="primary" size="small" fill-dot>
                   <v-card variant="tonal" color="primary" width="320px">
                    <v-card-title class="text-subtitle-1">19:30 - Missa Semanal</v-card-title>
                    <v-card-text class="text-caption">
                      <div>Igreja Matriz</div>
                      <div>Celebrante: Pe. Antônio Costa</div>
                    </v-card-text>
                  </v-card>
                </v-timeline-item>
              </v-timeline>
            </v-card-text>
          </v-card>
        </v-col>

        <v-divider vertical inset class="hidden-sm-and-down"></v-divider>

        <v-col cols="12" md="5">
           <v-card elevation="4" rounded="lg">
            <v-card-item class="bg-secondary">
              <v-card-title class="text-center text-h4 font-weight-medium">Eventos da Paróquia</v-card-title>
            </v-card-item>
            <v-card-text class="pa-4">
              <v-list lines="two" density="compact" class="bg-transparent">
                <v-list-item prepend-icon="mdi-party-popper" title="Festa Junina Paroquial" subtitle="20 de Julho de 2025 - Salão Paroquial"></v-list-item>
                <v-divider></v-divider>
                <v-list-item prepend-icon="mdi-meditation" title="Retiro Espiritual Anual" subtitle="15 a 17 de Agosto de 2025 - Casa de Retiros Bom Pastor"></v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Modules Section -->
    <div class="bg-secondary py-16">
      <v-container id="features">
        <h2 class="text-h3 font-weight-bold text-center mb-12">Módulos</h2>
        <v-row>
          <v-col v-for="module in modules" :key="module.title" cols="12" sm="6" lg="4">
            <NuxtLink :to="module.path || '#'" class="text-decoration-none">
              <v-card hover class="fill-height text-center pa-4" rounded="xl">
                <v-card-item>
                  <template #prepend>
                    <v-avatar :color="module.color || 'primary'" variant="tonal" size="large" class="mb-4">
                      <v-icon :icon="module.icon" size="x-large"></v-icon>
                    </v-avatar>
                  </template>
                </v-card-item>
                <v-card-title class="text-h6 font-weight-bold">{{ module.title }}</v-card-title>
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
          <v-img src="/logo.png" alt="Laudato System Logo" width="80%" class="mx-auto rounded-xl elevation-0" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/useAuthStore';
const authStore = useAuthStore();

const notices = ref([
  {
    icon: 'mdi-bell-ring',
    color: 'secondary',
    title: 'Campanha do Agasalho 2025',
    text: 'Estamos arrecadando agasalhos e cobertores para ajudar as famílias necessitadas da nossa comunidade. As doações podem ser entregues na secretaria paroquial até o dia 30 de Julho.'
  },
  {
    icon: 'mdi-book-open-page-variant',
    color: 'secondary',
    title: 'Inscrições para Catequese',
    text: 'As inscrições para a catequese de 2025 estão abertas! Procure a secretaria paroquial para mais informações e para realizar a inscrição de seus filhos.'
  }
]);

const modules = ref([
  {
    title: 'Missas e Liturgia',
    description: 'Gerencie celebrações, designe leitores, ministros, músicos e envie lembretes automáticos.',
    icon: 'mdi-calendar-clock',
    color: 'teal'
  },
  {
    title: 'Gestão de Usuários',
    description: 'Cadastre paroquianos, atribua funções, login seguro via e-mail, CPF ou ID de membro.',
    icon: 'mdi-account-group',
    color: 'light-blue'
  },
  {
    title: 'Eventos e Agenda Paroquial',
    description: 'Calendário completo com eventos, reuniões e horários de missas; reserva de espaços e notificações.',
    icon: 'mdi-calendar-multiselect',
    color: 'amber'
  },
  // {
  //   title: 'Biblioteca de Documentos',
  //   description: 'Carregue e organize documentos da igreja; PDFs de catecismo, vídeos e artigos.',
  //   icon: 'mdi-file-document-multiple',
  //   color: 'deep-orange'
  // },
  {
    title: 'Módulo Financeiro e de Doações',
    description: 'Gerencie dízimos, campanhas de arrecadação, gere relatórios e suporte doações online.',
    icon: 'mdi-cash-multiple',
    color: 'green'
  },
  {
    title: 'Catequese e Formação Cristã',
    description: 'Gerencie turmas, catequistas, controle de frequência e geração automática de certificados em PDF.',
    icon: 'mdi-school',
    color: 'purple'
  },
  {
    title: 'Comunicação Comunitária',
    description: 'Mural de notícias, mensagens em massa via WhatsApp/e-mail e integração com redes sociais.',
    icon: 'mdi-message-text',
    path: '/community',
    color: 'cyan'
  },
  {
    title: 'Pastorais e Movimentos',
    description: 'Cadastre grupos pastorais, agende reuniões e gerencie participantes.',
    icon: 'mdi-human-handsup',
    color: 'red'
  },
  {
    title: 'Módulo Devocional',
    description: 'Intenções de missa online, velas virtuais com intenções e áudio para novenas/orações.',
    icon: 'mdi-candle',
    path: '/devotional',
    color: 'yellow'
  },
]);

const { data: warnings } = useApi('/warnings/')

</script>
