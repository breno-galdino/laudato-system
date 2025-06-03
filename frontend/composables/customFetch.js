export const useApi = (request, opitons) => {
    const config = useRuntimeConfig()
    return useFetch(request, { baseURL: config.public.apiUrl, ...opitons })
  }