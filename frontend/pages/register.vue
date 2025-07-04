<template>
  <v-app>
    <v-main class="background-wrapper">
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="6" lg="4">
            <v-card style="border-radius: 15px;">
              <v-card-text>
                <div class="text-center mb-8">
                  <img src="/logo.png" alt="Logotipo" class="w-32 h-24 mx-auto">
                  <h1 class="text-3xl font-bold mt-4">Crie sua Conta</h1>
                </div>

                <v-form @submit.prevent="register">
                  <v-text-field v-model="newUser.name" label="Nome" prepend-inner-icon="mdi-account"
                    variant="outlined"></v-text-field>

                  <v-text-field v-model="newUser.email" label="Email" prepend-inner-icon="mdi-email"
                    variant="outlined"></v-text-field>

                  <v-text-field v-model="newUser.password" label="Senha" type="password" prepend-inner-icon="mdi-lock"
                    variant="outlined" :rules="passwordRules" class="mb-4"></v-text-field>

                  <v-btn type="submit" color="primary" class="text-white" block large>
                    REGISTRAR
                  </v-btn>

                  <div class="d-flex text-center align-center my-6">
                    <v-divider></v-divider>
                    <span class="mx-4 text-gray-500">OU</span>
                    <v-divider></v-divider>
                  </div>

                  <v-row>
                    <v-col cols="12" sm="6">
                      <v-btn color="#DB4437" class="text-white" block>
                        <v-icon left>mdi-google</v-icon>
                        Google
                      </v-btn>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-btn color="#4267B2" class="text-white" block>
                        <v-icon left>mdi-facebook</v-icon>
                        Facebook
                      </v-btn>
                    </v-col>
                  </v-row>

                  <div class="mt-8 text-center">
                    <span class="text-gray-600">Já tem uma conta?</span>
                    <a href="/login" class="ml-1 text-primary font-semibold hover:underline">
                      Acesse
                    </a>
                  </div>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
  import { ref } from 'vue';

  const newUser = ref({
    name: "",
    email: "",
    password: ""
  });

  const passwordRules = [
    v => !!v || 'A senha é obrigatória',
    v => (v && v.length >= 8) || 'A senha deve ter no mínimo 8 caracteres',
    v => /[!@#$%^&*(),.?":{}|<>]/.test(v) || 'A senha deve conter pelo menos um caractere especial'
  ];

  const register = () => {
    // Lógica de registro aqui
    console.log("Dados do novo usuário:", newUser.value);
  };
</script>

<style scoped>
  .background-wrapper {
    background: url("https://4kwallpapers.com/images/walls/thumbs_3t/13554.jpg") no-repeat center center;
    background-size: cover;
  }
</style>
