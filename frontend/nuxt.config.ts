export default defineNuxtConfig({
  future: {
    compatibilityVersion: 4,
  },

  app: {
    pageTransition: { name: 'page', mode: 'out-in' },
    baseURL: "/laudatosi",
  },

  modules: [
    "@nuxt/icon",
    "@nuxtjs/apollo",
    "@pinia/nuxt",
  ],

  pinia: {
    storesDirs: ["./app/stores/**"],
  },

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

  vite: {
    optimizeDeps: {
      include: [
        '@vue/devtools-core',
        '@vue/devtools-kit',
        'naive-ui',
        'apollo-upload-client/createUploadLink.mjs',
        '@apollo/client',
        '@vue/apollo-composable',
        'pinia',
      ],
    },
  },

  css: ["vuetify/styles"],

  build: {
    transpile: ["vuetify"],
  },

  runtimeConfig: {
    public: {
      apiUrl: process.env.API_URL,
    },
  },

  compatibilityDate: "2026-04-11",
});
