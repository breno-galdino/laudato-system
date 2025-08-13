export default defineNuxtConfig({
  app: {
    pageTransition: { name: 'page', mode: 'out-in' },
    baseURL: "/laudatosi",
  },
  
  modules: [
    "@nuxt/icon",
    [
      "@pinia/nuxt",
      {
        autoImports: ["defineStore", ["defineStore", "definePiniaStore"]],
      },
    ],
  ],

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

  compatibilityDate: "2025-05-15",
});
