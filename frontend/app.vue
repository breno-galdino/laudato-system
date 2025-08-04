<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup>
import { useAuthStore } from '@/stores/useAuthStore'
import { onMounted } from 'vue';

const authStore = useAuthStore()

onBeforeMount(() => {
  if (!authStore.isAuthenticated) {
    authStore.checkLogin();
  }
});
</script>