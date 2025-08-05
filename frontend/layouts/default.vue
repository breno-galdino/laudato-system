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
        <v-btn to="/login" color="primary">Entrar</v-btn>
        <v-btn to="/register" color="secondary">Cadastre-se</v-btn>
      </div>
      <div v-else class="mr-4">
        <v-btn class="text-none" to="/profile" prepend-icon="mdi-account-circle">{{authStore.user.username}}</v-btn>
      </div>
    </v-app-bar>

    <v-main class="h-100">
      <slot />
    </v-main>

    <v-footer class="d-flex flex-column ma-0 pa-0">
      <div class="d-flex justify-center w-100 align-center px-4">
        <v-btn v-for="icon in icons" :key="icon" class="mx-4" :icon="icon" variant="plain" size="small"></v-btn>
      </div>
      <div class="px-4 py-2 bg-black text-center w-100">
        {{ new Date().getFullYear() }} — <strong>Laudato System</strong>
      </div>
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