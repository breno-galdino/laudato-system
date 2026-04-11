export const useApi = (request, opitons) => {
  const config = useRuntimeConfig();
  return useFetch(request, { baseURL: config.public.apiUrl, ...opitons });
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
