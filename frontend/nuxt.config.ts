import tailwindcss from "@tailwindcss/vite";

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

  css: ["~/assets/css/main.css"],

  // build: {
  //   transpile: ["vuetify"],
  // },

  vite: {
    plugins: [tailwindcss()],
  },

  runtimeConfig: {
    public: {
      apiUrl: process.env.API_URL,
    },
  },

  compatibilityDate: "2025-05-15",
});
