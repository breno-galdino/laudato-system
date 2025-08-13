<template>
  <v-app>
    <v-main>
      <v-img src="https://4kwallpapers.com/images/walls/thumbs_3t/13554.jpg" cover class="h-screen">
        <v-container class="fill-height">
          <v-row justify="center">
            <v-col cols="12" sm="10" md="8" lg="7">
              <v-card class="elevation-12 rounded-xl">
                <v-row no-gutters>
                  <v-col cols="12" md="6" class="pa-8"
                    style="background: linear-gradient(135deg, #222831, #393E46); color: white;">
                    <div class="d-flex flex-column justify-center fill-height text-center">
                      <h2 class="text-h4 font-weight-bold">Bem Vindo!</h2>
                      <p class="mt-4">
                        Para se manter conectado conosco<br />
                        por favor acesse sua conta.
                      </p>
                    </div>
                  </v-col>
                  <v-col cols="12" md="6" class="pa-8">
                    <div class="text-center">
                      <v-img src="/logo.png" alt="Logotipo" height="96" contain class="mx-auto mb-4"></v-img>
                    </div>
                    <v-form @submit.prevent="login">
                      <v-text-field v-model="credentialUser.username" label="Email" prepend-inner-icon="mdi-email"
                        variant="solo-filled" hide-details class="mb-3" />
                      <v-text-field v-model="credentialUser.password" label="Senha" type="password"
                        prepend-inner-icon="mdi-lock" variant="solo-filled" hide-details class="mb-3" />
                      <v-btn type="submit" color="primary" class="mt-4" :loading="loading" block>
                        ENTRAR
                      </v-btn>
                      <div class="mt-4 text-center">
                        <span>Não tem uma conta?</span>
                        <router-link to="/register" class="ml-1 text-primary font-weight-bold">Registre-se</router-link>
                      </div>
                    </v-form>
                  </v-col>
                </v-row>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-img>
    </v-main>
  </v-app>
</template>

<script setup>
  import { useAuthStore } from '../stores/useAuthStore';
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated;

  const credentialUser = ref({
    username: "",
    password: ""
  })

  const loading = ref(false);

  const router = useRouter();

  const login = async () => {
    loading.value = true;
    try {
      await authStore.login(credentialUser.value.username, credentialUser.value.password);
      router.push('/profile');
    } catch (error) {
      console.error("Login failed:", error);
      // Handle login error (e.g., show a message to the user)
    } finally {
      loading.value = false;
    }
  }
</script>