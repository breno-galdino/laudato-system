<template>
  <v-app>
    <v-main>
      <v-img src="https://4kwallpapers.com/images/walls/thumbs_3t/13554.jpg" cover class="h-screen">
        <v-container class="fill-height">
          <v-row justify="center">
            <v-col cols="12" sm="10" md="8" lg="5">
              <v-card class="elevation-12 rounded-xl pa-4">
                <v-card-text>
                  <div class="text-center mb-8">
                    <v-img src="/logo.png" alt="Logotipo" height="96" contain class="mx-auto"></v-img>
                    <h1 class="text-h4 font-weight-bold mt-4">Crie sua Conta</h1>
                  </div>

                  <v-form @submit.prevent="register">
                    <v-text-field v-model="newUser.name" label="Nome" prepend-inner-icon="mdi-account"
                      variant="outlined"></v-text-field>

                    <v-text-field v-model="newUser.email" label="Email" prepend-inner-icon="mdi-email"
                      variant="outlined"></v-text-field>

                    <v-text-field v-model="newUser.password" label="Senha" type="password" prepend-inner-icon="mdi-lock"
                      variant="outlined" :rules="passwordRules" class="mb-4"></v-text-field>

                    <v-btn type="submit" color="primary" block size="large">
                      REGISTRAR
                    </v-btn>

                    <v-divider class="my-6">
                      <span class="text-caption">OU</span>
                    </v-divider>

                    <v-row>
                      <v-col cols="12" sm="6">
                        <v-btn color="#DB4437" block>
                          <v-icon start>mdi-google</v-icon>
                          Google
                        </v-btn>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-btn color="#4267B2" block>
                          <v-icon start>mdi-facebook</v-icon>
                          Facebook
                        </v-btn>
                      </v-col>
                    </v-row>

                    <div class="mt-8 text-center">
                      <span>Já tem uma conta?</span>
                      <router-link to="/login" class="ml-1 text-primary font-weight-bold">Acesse</router-link>
                    </div>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-img>
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