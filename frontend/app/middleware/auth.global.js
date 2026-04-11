import { useAuthStore } from '~/stores/useAuthStore.js';

export default defineNuxtRouteMiddleware((to, from) => {
  const userStore = useAuthStore();
  const isAuthenticated = userStore?.isAuthenticated;
  const isPublicRoute = to.path === "/login" || to.path === "/register" || to.path === "/";
  if (!isAuthenticated && !isPublicRoute) {
    console.log("Usuário não autenticado, redirecionando para login");
    return navigateTo("/login");
  }
});
