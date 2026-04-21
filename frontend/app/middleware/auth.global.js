import { useAuthStore } from '~/stores/useAuthStore.js';

// Rotas estáticas públicas
const PUBLIC_STATIC = ["/", "/login", "/register", "/register-parish"];

// Prefixos de rotas públicas (ex: /:slug é sempre público)
const PUBLIC_PREFIXES = ["/parish/"];

export default defineNuxtRouteMiddleware((to, from) => {
  const userStore = useAuthStore();
  const isAuthenticated = userStore?.isAuthenticated;

  // Rotas estáticas conhecidas
  if (PUBLIC_STATIC.includes(to.path)) return;

  // Prefixos públicos
  if (PUBLIC_PREFIXES.some(prefix => to.path.startsWith(prefix))) return;

  // Rota dinâmica de paróquia: /:slug (um único segmento sem barra)
  const segments = to.path.split("/").filter(Boolean);
  if (segments.length === 1) return;

  if (!isAuthenticated) {
    return navigateTo("/login");
  }
});
