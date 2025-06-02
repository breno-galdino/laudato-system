export const useApi = (request, opts) => {
    const config = useRuntimeConfig()
    return useFetch(request, { baseURL: config.public.apiUrl, ...opts })
  }