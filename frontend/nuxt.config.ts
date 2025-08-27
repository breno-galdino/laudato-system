export default defineNuxtConfig({
  app: {
    pageTransition: { name: 'page', mode: 'out-in' },
    baseURL: "/laudatosi",
  },
  
  modules: [
    "@nuxt/icon", '@nuxtjs/apollo',
    [
      "@pinia/nuxt",
      {
        autoImports: ["defineStore", ["defineStore", "definePiniaStore"]],
      },
    ],
  ],

  apollo: {
    clients: {
      default: {
        httpEndpoint: process.env.API_URL + "graphql",
        tokenStorage: "cookie",
        httpLinkOptions: {
          credentials: "include",
        },
        inMemoryCacheOptions: {
          addTypename: false,
        },
      },
    },
  },

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
