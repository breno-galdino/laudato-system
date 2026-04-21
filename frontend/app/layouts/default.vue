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
      <template v-if="authStore.user">
        <v-btn size="small" to="/community" class="text-none">Comunidade</v-btn>
        <v-btn size="small" to="/devotional" class="text-none">Devocional</v-btn>
        <v-btn v-if="authStore.canManage" size="small" to="/management" class="text-none">Gestão</v-btn>
      </template>
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

    <v-footer class="bg-blue-grey-darken-4 text-white footer-compact" padless>
      <v-container>
        <!-- Paróquia: nome, diocese e redes sociais centralizados -->
        <template v-if="authStore.parish?.name">
          <v-row justify="center" class="pb-2">
            <v-col cols="12" class="text-center">
              <p class="text-h6 font-weight-bold mb-0">{{ authStore.parish.name }}</p>
              <p v-if="authStore.parish?.diocese_name" class="text-caption text-blue-grey-lighten-3 mt-1">
                {{ authStore.parish.diocese_name }}
              </p>
              <div v-if="hasSocial" class="d-flex justify-center ga-1 mt-3">
                <v-btn
                  v-if="authStore.parish?.facebook_url"
                  icon size="small" variant="text" color="white"
                  :href="authStore.parish.facebook_url" target="_blank"
                >
                  <v-icon size="20">mdi-facebook</v-icon>
                </v-btn>
                <v-btn
                  v-if="authStore.parish?.instagram_url"
                  icon size="small" variant="text" color="white"
                  :href="authStore.parish.instagram_url" target="_blank"
                >
                  <v-icon size="20">mdi-instagram</v-icon>
                </v-btn>
                <v-btn
                  v-if="authStore.parish?.youtube_url"
                  icon size="small" variant="text" color="white"
                  :href="authStore.parish.youtube_url" target="_blank"
                >
                  <v-icon size="20">mdi-youtube</v-icon>
                </v-btn>
                <v-btn
                  v-if="authStore.parish?.whatsapp"
                  icon size="small" variant="text" color="white"
                  :href="`https://wa.me/${authStore.parish.whatsapp.replace(/\D/g,'')}`" target="_blank"
                >
                  <v-icon size="20">mdi-whatsapp</v-icon>
                </v-btn>
              </div>
            </v-col>
          </v-row>
          <v-divider class="mb-3 mt-2" color="rgba(255,255,255,0.15)" />
        </template>

        <!-- Copyright -->
        <v-row justify="center" :class="authStore.parish?.name ? 'pb-3' : 'py-4'">
          <v-col cols="12" class="text-center text-caption text-blue-grey-lighten-2">
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

  const hasSocial = computed(() => {
    const p = authStore.parish;
    return !!(p?.facebook_url || p?.instagram_url || p?.youtube_url || p?.whatsapp);
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

.footer-compact {
  min-height: unset;
}
</style>