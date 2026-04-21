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
      <v-toolbar-title>
        <v-img src="/laudato.png" height="48px" width="48px"></v-img>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn size="small" class="text-none" to="/" exact>Início</v-btn>
      <v-btn size="small" to="/community" class="text-none">Comunidade</v-btn>
      <v-btn size="small" to="/devotional" class="text-none">Devocional</v-btn>
      <v-btn size="small" to="/management" class="text-none">Gestão</v-btn>
      <div v-if="!authStore.user" class="ml-4">
        <v-btn size="small" to="/login" color="accent" class="text-none" rounded>Entrar</v-btn>
        <v-btn size="small" to="/register" color="accent" class="text-none" rounded>Cadastre-se</v-btn>
      </div>
      <div v-else class="d-flex align-center ga-2 mr-3">
        <v-chip
          v-if="authStore.parish?.name"
          prepend-icon="mdi-church"
          variant="tonal"
          color="white"
          size="small"
          class="hidden-sm-and-down parish-chip"
        >
          {{ authStore.parish.name }}
        </v-chip>
        <v-btn class="text-none" to="/profile" prepend-icon="mdi-account-circle" size="small">
          {{ authStore.user.username }}
        </v-btn>
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
            <h4 class="text-h6 font-weight-bold mb-2">{{ authStore.parish?.name || 'Laudato System' }}</h4>
            <p v-if="authStore.parish?.address" class="text-body-2">
              {{ authStore.parish.address }}
            </p>
            <p v-if="authStore.parish?.email" class="text-body-2 mt-2">
              <v-icon start size="small">mdi-email</v-icon>
              {{ authStore.parish.email }}
            </p>
            <p v-if="authStore.parish?.phone" class="text-body-2">
              <v-icon start size="small">mdi-phone</v-icon>
              {{ authStore.parish.phone }}
            </p>
          </v-col>

          <!-- Coluna 2: Links úteis -->
          <v-col cols="12" md="4">
            <h4 class="text-h6 font-weight-bold mb-2">Links úteis</h4>
            <v-list density="compact" nav class="bg-transparent">
              <v-list-item title="Sobre a Plataforma" prepend-icon="mdi-information-outline" />
              <v-list-item title="Fale Conosco" prepend-icon="mdi-email-outline" />
              <v-list-item title="Política de Privacidade" prepend-icon="mdi-shield-lock-outline" />
              <v-list-item title="Termos de Uso" prepend-icon="mdi-file-document-outline" />
            </v-list>
          </v-col>

          <!-- Coluna 3: Redes sociais -->
          <v-col cols="12" md="4">
            <h4 class="text-h6 font-weight-bold mb-2">Siga-nos</h4>
            <div class="d-flex ga-4">
              <v-btn icon size="small" variant="text" color="white">
                <v-icon size="24">mdi-facebook</v-icon>
              </v-btn>
              <v-btn icon size="small" variant="text" color="white">
                <v-icon size="24">mdi-instagram</v-icon>
              </v-btn>
              <v-btn icon size="small" variant="text" color="white">
                <v-icon size="24">mdi-youtube</v-icon>
              </v-btn>
              <v-btn icon size="small" variant="text" color="white">
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
  import { useAuthStore } from '~/stores/useAuthStore.js';
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

<style scoped>
.parish-chip {
  opacity: 0.85;
  border: 1px solid rgba(255,255,255,0.3);
  max-width: 220px;
}

.parish-chip :deep(.v-chip__content) {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>