import { useAuthStore } from '../stores/useAuthStore.js';

export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore();

  if (!authStore.user) {
    try {
      await authStore.checkLogin();
    } catch (err) {
      console.log("Usuário não autenticado.");
    }
  }
});
