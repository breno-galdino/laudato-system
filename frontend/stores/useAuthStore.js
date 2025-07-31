import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    loading: false,
  }),

  actions: {
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
          credentials: "include",
        });
        await this.fetchUser();

        const router = useRouter();
        router.push("/");
      } catch (err) {
        console.error("Erro ao fazer login:", err);
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async fetchUser() {
      try {
        const { data } = await asyncUseApi("/auth/profile");

        console.log(data.value);
        this.user = data.value || null;
      } catch (err) {
        console.error("Erro ao buscar usuário:", err);
        this.user = null;
      }
    },

    async logout() {
      try {
        await $fetch("/auth/logout", {
          method: "POST",
          credentials: "include",
        });
      } catch (err) {
        console.error("Erro ao fazer logout:", err);
      }
      this.user = null;
    },
  },
});
