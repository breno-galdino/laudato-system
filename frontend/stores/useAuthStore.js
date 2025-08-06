import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    loading: false,
    isAuthenticated: false
  }),

  actions: {
    async checkLogin() {
      try {
        await this.fetchUser();
      } catch (err) {
        console.error("Erro ao verificar login:", err);
      } 
    },
    async login(username, password) {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      this.loading = true;
      try {
        const { data } = await asyncUseApi("/auth/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: formData,
        });
        await this.fetchUser();

      } catch (err) {
        console.error("Erro ao fazer login:", err);
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async fetchUser() {
      try {
        const { data } = await asyncUseApi("/auth/me", {
          onResponse({ request, response, options }) {
            // Handle response if needed
          },
        });
        this.user = data.value || null;
        this.isAuthenticated = !!this.user;
      } catch (err) {
        console.error("Erro ao buscar usuário:", err);
        this.user = null;
        this.isAuthenticated = !!this.user;
      }
    },

    async logout() {
      try {
        await asyncUseApi("/auth/logout");
      } catch (err) {
        console.error("Erro ao fazer logout:", err);
      }
      this.user = null;
      this.isAuthenticated = false;
    },
  },
});
