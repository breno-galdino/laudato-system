export const useApi = (request, options) => {
  const config = useRuntimeConfig();
  return useFetch(request, { baseURL: config.public.apiUrl, ...options });
};

export const asyncUseApi = async (request, options) => {
  const config = useRuntimeConfig();
  return await useFetch(request, {
    baseURL: config.public.apiUrl,
    credentials: "include",
    server: false,
    ...options,
  });
};

/**
 * Variante pública que injeta automaticamente ?parish_slug=<slug>.
 * Se não houver paróquia no contexto, retorna { data: ref([]) } sem chamar a API.
 */
export const asyncPublicApi = async (endpoint, options) => {
  const { useAuthStore } = await import('~/stores/useAuthStore.js');
  const authStore = useAuthStore();
  const slug = authStore.parishSlug;

  if (!slug) {
    return { data: ref([]), error: ref(null) };
  }

  const url = `${endpoint}${endpoint.includes('?') ? '&' : '?'}parish_slug=${slug}`;
  return asyncUseApi(url, options);
};
