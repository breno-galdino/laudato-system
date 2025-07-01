// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,

  css: ["vuetify/lib/styles/main.sass"],

  build: {
    transpile: ["vuetify"],
  },

  runtimeConfig: {
    public: {
      apiUrl: process.env.API_URL,
    },
  },
  
  compatibilityDate: '2025-05-15'
})
