<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup>
import { useAuthStore } from '@/stores/useAuthStore'

const authStore = useAuthStore()

onBeforeMount(() => {
  if (!authStore.isAuthenticated) {
    authStore.checkLogin();
  }
});
</script>