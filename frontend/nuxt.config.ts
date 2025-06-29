// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    "@nuxtjs/tailwindcss",
    "@nuxt/icon",
    [
      "@pinia/nuxt",
      {
        autoImports: ["defineStore", ["defineStore", "definePiniaStore"]],
      },
    ],
  ],

  ssr: false,

  runtimeConfig: {
    public: {
      apiUrl: process.env.API_URL,
    },
  },
  
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true }
})
