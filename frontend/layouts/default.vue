<template>
  <v-app>
    <!-- <v-navigation-drawer v-model="drawer" expand-on-hover rail permanent color="black">
      <v-list density="compact" nav v-if="authStore.user">
        <v-list-item :title="authStore?.user?.username.split(' ')[0]" :subtitle="authStore?.user?.full_name" nav>
          <template #prepend>
            <v-icon size="large">mdi-account-circle</v-icon>
          </template>
<template #append>
            <v-btn icon variant="text" size="small" to="/profile"><v-icon>mdi-cog</v-icon></v-btn>
          </template>
</v-list-item>
</v-list>


<v-divider></v-divider>

<v-list density="compact" nav>
  <v-list-item prepend-icon="mdi-home" title="Início" value="inbox" to="/"></v-list-item>
  <v-list-item prepend-icon="mdi-account-group" title="Comunidade" value="supervisors" to="/community"></v-list-item>
  <v-list-item prepend-icon="mdi-book-open-page-variant" title="Devocional" value="devotional"
    to="/devotional"></v-list-item>
  <v-list-item prepend-icon="mdi-cog" title="Gestão" value="management" to="/management"></v-list-item>
  <v-list-item prepend-icon="mdi-email" title="Contato" value="contact" to="/contact"></v-list-item>
</v-list>
</v-navigation-drawer> -->

    <v-app-bar elevation="0" color="primary">
      <v-app-bar-nav-icon @click="drawer = !drawer" class="d-md-none"></v-app-bar-nav-icon>
      <v-toolbar-title><v-img src="/laudato.png" height="64px" width="64px"></v-img></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn size="small" class="text-none" to="/" exact>Início</v-btn>
      <v-btn size="small" to="/community" class="text-none">Comunidade</v-btn>
      <v-btn size="small" to="/devotional" class="text-none">Devocional</v-btn>
      <v-btn size="small" to="/management" class="text-none">Gestão</v-btn>
      <div v-if="!authStore.user" class="ml-4">
        <v-btn size="small" to="/login" color="accent" class="text-none" rounded>Entrar</v-btn>
        <v-btn size="small" to="/register" color="accent" class="text-none" rounded>Cadastre-se</v-btn>
      </div>
      <div v-else class="mr-4">
        <v-btn class="text-none" to="/profile" prepend-icon="mdi-account-circle">{{ authStore.user.username }}</v-btn>
      </div>
    </v-app-bar>

    <v-main>
      <slot />
    </v-main>

    <v-footer class="bg-blue-grey-darken-4 text-white pt-10" padless>
      <v-container>
        <v-row class="px-2" justify="space-between" align="start">
          <!-- Coluna 1: Informações da Paróquia -->
          <v-col cols="12" md="4">
            <h4 class="text-h6 font-weight-bold mb-2">Paróquia São João Batista</h4>
            <p class="text-body-2">
              Rua das Flores, 123<br>
              Centro - Cidade/UF<br>
              CEP: 00000-000
            </p>
            <p class="text-body-2 mt-2">
              <v-icon start size="small">mdi-email</v-icon>
              contato@paroquia.com.br
            </p>
            <p class="text-body-2">
              <v-icon start size="small">mdi-phone</v-icon>
              (11) 1234-5678
            </p>
          </v-col>

          <!-- Coluna 2: Links úteis -->
          <v-col cols="12" md="4">
            <h4 class="text-h6 font-weight-bold mb-2">Links úteis</h4>
            <v-list density="compact" nav class="bg-transparent">
              <v-list-item to="/about" title="Sobre a Plataforma" prepend-icon="mdi-information-outline" />
              <v-list-item to="/contact" title="Fale Conosco" prepend-icon="mdi-email-outline" />
              <v-list-item to="/privacy" title="Política de Privacidade" prepend-icon="mdi-shield-lock-outline" />
              <v-list-item to="/terms" title="Termos de Uso" prepend-icon="mdi-file-document-outline" />
            </v-list>
          </v-col>

          <!-- Coluna 3: Redes sociais -->
          <v-col cols="12" md="4">
            <h4 class="text-h6 font-weight-bold mb-2">Siga-nos</h4>
            <div class="d-flex ga-4">
              <v-btn icon size="small" variant="text" color="white" href="https://facebook.com" target="_blank">
                <v-icon size="24">mdi-facebook</v-icon>
              </v-btn>
              <v-btn icon size="small" variant="text" color="white" href="https://instagram.com" target="_blank">
                <v-icon size="24">mdi-instagram</v-icon>
              </v-btn>
              <v-btn icon size="small" variant="text" color="white" href="https://youtube.com" target="_blank">
                <v-icon size="24">mdi-youtube</v-icon>
              </v-btn>
              <v-btn icon size="small" variant="text" color="white" href="https://wa.me/5511999999999" target="_blank">
                <v-icon size="24">mdi-whatsapp</v-icon>
              </v-btn>
            </div>
          </v-col>
        </v-row>

        <v-divider class="my-4" color="white" />

        <!-- Copyright -->
        <v-row justify="center" class="pb-2">
          <v-col cols="12" class="text-center text-caption text-white">
            © {{ new Date().getFullYear() }} Laudato System — Todos os direitos reservados.
          </v-col>
        </v-row>
      </v-container>
    </v-footer>

  </v-app>
</template>

<script setup>
  import { useAuthStore } from '@/stores/useAuthStore';

  const authStore = useAuthStore();
  const drawer = ref(true);
  const rail = ref(true);

  const icons = [
    'mdi-facebook',
    'mdi-twitter',
    'mdi-linkedin',
    'mdi-instagram',
  ];

  onMounted(() => {
    if (window.innerWidth < 960) {
      drawer.value = false;
    }
  });
</script>