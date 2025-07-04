<template>
  <div>
    <!-- Hero Section -->
    <div class="relative">
      <div class="bg-cover bg-center h-[500px]" style="background-image: url('/diocese.png');">
        <div class="bg-gradient-to-r from-[#2C3E50] to-[#000] bg-opacity-70 h-full flex items-center justify-center">
          <div class="text-center text-white p-8 rounded-lg shadow-xl">
            <h1 class="text-5xl font-extrabold mb-4 leading-tight">Plataforma de Gestão Paroquial Católica</h1>
            <p class="text-xl mb-8 opacity-90">Uma solução unificada para administração simplificada e engajamento
              comunitário vibrante.</p>
            <div>
                <div class="flex flex-col md:flex-row justify-center items-center gap-4">
                <a
                  href="#features"
                  class="w-60 h-12 flex items-center justify-center rounded-full font-bold bg-white text-[#2C3E50] border border-[#3498DB] shadow transition-all duration-200 hover:scale-105 hover:bg-[#CCC] hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-[#3498DB]"
                >
                  Saiba Mais
                </a>
                <a
                  href="/login"
                  class="w-60 h-12 flex items-center justify-center rounded-full font-bold bg-[#3498DB] text-white shadow transition-all duration-200 hover:bg-[#217dbb] hover:scale-105 hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-[#3498DB]"
                >
                  Acessar Sistema
                </a>
                </div>


            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Important Notices Section -->
    <section class="py-10">
      <div class="container mx-auto px-6">
        <h2 class="text-4xl font-bold text-center" style="color: #2C3E50;">Avisos Importantes</h2>
        <v-card class="mx-auto mt-10" width="100%"
          style="background-color: #FFFFFF; border: 1px solid #BDC3C7; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: all 0.3s ease-in-out;"
          hover>
          <v-card-title class="text-h5" style="color: rgb(var(--v-theme-primary)); font-weight: bold;">Campanha do
            Agasalho
            2025</v-card-title>
          <v-card-text style="color: #2C3E50;">
            Estamos arrecadando agasalhos e cobertores para ajudar as famílias necessitadas da nossa comunidade. As
            doações podem ser entregues na secretaria paroquial até o dia 30 de Julho.
          </v-card-text>
          <v-divider></v-divider>
          <v-card-title class="text-h5" style="color: rgb(var(--v-theme-primary)); font-weight: bold;">Inscrições para
            Catequese</v-card-title>
          <v-card-text style="color: #2C3E50;">
            As inscrições para a catequese de 2025 estão abertas! Procure a secretaria paroquial para mais informações e
            para realizar a inscrição de seus filhos.
          </v-card-text>
        </v-card>
      </div>
    </section>
    <v-divider :thickness="5"></v-divider>

    <!-- Masses and Events Section -->
    <section class="py-10">
      <div class="container mx-auto px-2">
        <h2 class="text-4xl font-bold text-center mt-2 mb-8" style="color: #2C3E50;">Calendário Paroquial</h2>
        <v-row justify="center" align="start" class="gap-6">
          <v-col cols="12" md="4">
            <h3 class="text-3xl font-bold mb-8" style="color: #2C3E50;">Próximas Missas</h3>
            <div class="space-y-8">
              <v-card class="mx-auto bg-secondary" width="100%"
                style="border: 1px solid #BDC3C7; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: all 0.3s ease-in-out;"
                hover>
                <v-card-title class="text-h5" style="font-weight: bold;">Missa Dominical</v-card-title>
                <v-card-text>
                  <div class="d-flex align-center mb-2">
                    <v-icon color="#3498DB" class="mr-2">mdi-calendar-clock</v-icon>
                    <span>Domingo, 09:00 - Igreja Matriz</span>
                  </div>
                  <div class="d-flex align-center">
                    <v-icon color="#3498DB" class="mr-2">mdi-account-tie</v-icon>
                    <span>Celebrante: Pe. João Silva</span>
                  </div>
                </v-card-text>
              </v-card>
              <v-card class="mx-auto bg-secondary" width="100%"
                style="border: 1px solid #BDC3C7; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: all 0.3s ease-in-out;"
                hover>
                <v-card-title class="text-h5" style="font-weight: bold;">Missa da Família</v-card-title>
                <v-card-text>
                  <div class="d-flex align-center mb-2">
                    <v-icon color="#3498DB" class="mr-2">mdi-calendar-clock</v-icon>
                    <span>Sábado, 18:00 - Capela São José</span>
                  </div>
                  <div class="d-flex align-center">
                    <v-icon color="#3498DB" class="mr-2">mdi-account-tie</v-icon>
                    <span>Celebrante: Pe. Pedro Santos</span>
                  </div>
                </v-card-text>
              </v-card>
              <v-card class="mx-auto bg-secondary" width="100%"
                style="border: 1px solid #BDC3C7; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: all 0.3s ease-in-out;"
                hover>
                <v-card-title class="text-h5" style="font-weight: bold;">Missa Semanal</v-card-title>
                <v-card-text>
                  <div class="d-flex align-center mb-2">
                    <v-icon color="#3498DB" class="mr-2">mdi-calendar-clock</v-icon>
                    <span>Quarta-feira, 19:30 - Igreja Matriz</span>
                  </div>
                  <div class="d-flex align-center">
                    <v-icon color="#3498DB" class="mr-2">mdi-account-tie</v-icon>
                    <span>Celebrante: Pe. Antônio Costa</span>
                  </div>
                </v-card-text>
              </v-card>
            </div>
          </v-col>
          <v-divider vertical class="my-4"></v-divider>
          <v-col cols="12" md="4">
            <h3 class="text-3xl font-bold mb-8" align="end" style="color: #2C3E50;">Eventos da Paróquia</h3>
            <div class="space-y-8">
              <v-card class="mx-auto bg-secondary" width="100%"
                style="border: 1px solid #BDC3C7; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: all 0.3s ease-in-out;"
                hover>
                <v-card-title class="text-h5" style="font-weight: bold;">Festa Junina
                  Paroquial</v-card-title>
                <v-card-text>
                  <div class="d-flex align-center mb-2">
                    <v-icon color="#3498DB" class="mr-2">mdi-calendar-range</v-icon>
                    <span>Data: 20 de Julho de 2025</span>
                  </div>
                  <div class="d-flex align-center mb-2">
                    <v-icon color="#3498DB" class="mr-2">mdi-map-marker</v-icon>
                    <span>Local: Salão Paroquial</span>
                  </div>
                  <div class="d-flex align-center">
                    <v-icon color="#3498DB" class="mr-2">mdi-star-four-points</v-icon>
                    <span>Atrações: Comidas típicas, quadrilha, música ao vivo.</span>
                  </div>
                </v-card-text>
              </v-card>
              <v-card class="mx-auto bg-secondary" width="100%"
                style="border: 1px solid #BDC3C7; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: all 0.3s ease-in-out;"
                hover>
                <v-card-title class="text-h5" style="font-weight: bold;">Retiro Espiritual
                  Anual</v-card-title>
                <v-card-text>
                  <div class="d-flex align-center mb-2">
                    <v-icon color="#3498DB" class="mr-2">mdi-calendar-range</v-icon>
                    <span>Data: 15 a 17 de Agosto de 2025</span>
                  </div>
                  <div class="d-flex align-center mb-2">
                    <v-icon color="#3498DB" class="mr-2">mdi-map-marker</v-icon>
                    <span>Local: Casa de Retiros Bom Pastor</span>
                  </div>
                  <div class="d-flex align-center">
                    <v-icon color="#3498DB" class="mr-2">mdi-theme-light-dark</v-icon>
                    <span>Tema: Fé e Caridade no Mundo Atual.</span>
                  </div>
                </v-card-text>
              </v-card>
            </div>
          </v-col>
        </v-row>
      </div>
    </section>
    <v-divider :thickness="5"></v-divider>

    <!-- Modules Section -->
    <section id="features" class="py-10" style="background-color: #B0BEC590;">
      <div class="container mx-auto px-6">
        <h2 class="text-4xl font-bold text-center" style="color: #2C3E50;">Módulos Principais</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10 mt-10">
          <NuxtLink v-for="module in modules" :key="module.title" :to="module.path || '#'">
            <div
              class="bg-white p-8 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 ease-in-out h-full"
              style="border: 1px solid #BDC3C7;">
              <div class="flex items-center mb-5">
                <Icon :name="module.icon" class="text-4xl" style="color: #3498DB;" />
                <h3 class="text-2xl font-bold ml-4" style="color: #2C3E50;">{{ module.title }}</h3>
              </div>
              <p class="leading-relaxed" style="color: #2C3E50;">{{ module.description }}</p>
            </div>
          </NuxtLink>
        </div>
      </div>
    </section>
    <v-divider :thickness="5"></v-divider>

    <!-- Special Emphasis Section -->
    <section class="py-20">
      <div class="container mx-auto px-6">
        <div class="grid md:grid-cols-2 gap-12 items-center">
          <div class="text-center md:text-left">
            <h2 class="text-4xl font-bold mb-6 leading-tight" style="color: #2C3E50;">Nutrindo a Fé e a Comunidade</h2>
            <p class="mb-8 text-lg leading-relaxed" style="color: #2C3E50;">Nossa plataforma foi projetada para
              fortalecer os laços de sua comunidade paroquial e fornecer ferramentas para o crescimento espiritual na
              era digital.</p>
            <div class="space-y-8">
              <div>
                <div class="flex items-center mb-3">
                  <Icon name="mdi:message-text" class="text-4xl" style="color: #3498DB;" />
                  <h3 class="text-2xl font-bold ml-4" style="color: #2C3E50;">Comunicação Comunitária</h3>
                </div>
                <p class="leading-relaxed" style="color: #2C3E50;">Mantenha seus paroquianos informados e engajados com
                  nossas ferramentas de comunicação integradas. Envie mensagens em massa, compartilhe notícias e
                  conecte-se com sua comunidade nas redes sociais.</p>
              </div>
              <div>
                <div class="flex items-center mb-3">
                  <Icon name="mdi:candle" class="text-4xl" style="color: #3498DB;" />
                  <h3 class="text-2xl font-bold ml-4" style="color: #2C3E50;">Ferramentas Devocionais</h3>
                </div>
                <p class="leading-relaxed" style="color: #2C3E50;">Promova uma vida de oração com intenções de missa
                  online, velas virtuais e uma biblioteca de novenas e orações. Forneça aos seus paroquianos recursos
                  para nutrir sua fé de qualquer lugar.</p>
              </div>
            </div>
          </div>
          <div class="text-center">
            <img src="/logo.png" alt="Laudato System Logo"
              class="mx-auto rounded-xl shadow-2xl w-2/3 transform hover:scale-105 transition-transform duration-300 ease-in-out">
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
  import { ref } from 'vue';

  const modules = ref([
    {
      title: 'Agendamento de Missas e Liturgia',
      description: 'Gerencie celebrações, designe leitores, ministros, músicos e envie lembretes automáticos.',
      icon: 'mdi:calendar-clock',
    },
    {
      title: 'Gestão de Usuários e Permissões',
      description: 'Cadastre paroquianos, atribua funções, login seguro via e-mail, CPF ou ID de membro.',
      icon: 'mdi:account-group',
    },
    {
      title: 'Eventos e Agenda Paroquial',
      description: 'Calendário completo com eventos, reuniões e horários de missas; reserva de espaços e notificações.',
      icon: 'mdi:calendar-multiselect',
    },
    {
      title: 'Biblioteca de Documentos e Conteúdo',
      description: 'Carregue e organize documentos da igreja; PDFs de catecismo, vídeos e artigos.',
      icon: 'mdi:file-document-multiple',
    },
    {
      title: 'Módulo Financeiro e de Doações',
      description: 'Gerencie dízimos, campanhas de arrecadação, gere relatórios e suporte doações online.',
      icon: 'mdi:cash-multiple',
    },
    {
      title: 'Catequese e Formação Cristã',
      description: 'Gerencie turmas, catequistas, controle de frequência e geração automática de certificados em PDF.',
      icon: 'mdi:school',
    },
    {
      title: 'Comunicação Comunitária',
      description: 'Mural de notícias, mensagens em massa via WhatsApp/e-mail e integração com redes sociais.',
      icon: 'mdi:message-text',
      path: '/community'
    },
    {
      title: 'Registro de Sacramentos',
      description: 'Acompanhe o histórico sacramental individual e emita certificados (batismo, confirmação, casamento).',
      icon: 'mdi:book-open-page-variant',
    },
    {
      title: 'Gestão de Pastorais e Movimentos',
      description: 'Cadastre grupos pastorais, agende reuniões e gerencie participantes.',
      icon: 'mdi:human-handsup',
    },
    {
      title: 'Módulo Devocional',
      description: 'Intenções de missa online, velas virtuais com intenções e áudio para novenas/orações.',
      icon: 'mdi:candle',
      path: '/devotional'
    },
  ]);
</script>

<style>
  /* You can add any additional global styles here if needed */
</style>
