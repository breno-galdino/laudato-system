import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "@mdi/font/css/materialdesignicons.css";

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = createVuetify({
    components,
    directives,
    icons: { defaultSet: "mdi" },
    theme: {
      defaultTheme: "light",
      themes: {
        light: {
          dark: false,
          colors: {
            primary: "#212b59",
            secondary: "#222",
            accent: "#E5E5E5",
            success: "#3f8255",
            warning: "#dfb256",
            error: "#c6453a",
            info: "#222",
          },
        },
        dark: {
          dark: true,
          colors: {
            primary: "#FFFFFF",
            secondary: "#113311",
            accent: "#0F0F0F",
            success: "#44AA44",
            warning: "#FFCC66",
            error: "#FF6666",
            info: "#113344",
          },
        },
      },
    },
  });

  nuxtApp.vueApp.use(vuetify);
});
