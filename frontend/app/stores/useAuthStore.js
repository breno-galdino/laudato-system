import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    parish: null,
    loading: false,
    isAuthenticated: false,
  }),

  getters: {
    parishSlug: (state) => state.parish?.slug ?? null,
  },

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
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: formData,
        });

        if (data.value) {
          this.parish = {
            id: data.value.parish_id,
            slug: data.value.parish_slug,
            name: data.value.parish_name,
          };
        }

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
        const { data } = await asyncUseApi("/auth/me");
        this.user = data.value || null;
        this.isAuthenticated = !!this.user;

        if (this.user && !this.parish) {
          await this.fetchParish();
        }
      } catch (err) {
        this.user = null;
        this.isAuthenticated = false;
      }
    },

    async fetchParish() {
      try {
        const { data } = await asyncUseApi("/parish/me");
        if (data.value) {
          this.parish = data.value;
        }
      } catch (err) {
        console.error("Erro ao buscar paróquia:", err);
      }
    },

    async logout() {
      try {
        await asyncUseApi("/auth/logout");
      } catch (err) {
        console.error("Erro ao fazer logout:", err);
      }
      this.user = null;
      this.parish = null;
      this.isAuthenticated = false;
    },
  },
});
