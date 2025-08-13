<template>
  <v-app>
    <v-main class="bg-grey-lighten-4">
      <v-img src="https://4kwallpapers.com/images/walls/thumbs_3t/13554.jpg" cover class="h-screen">
        <v-container class="fill-height" fluid>
          <v-row align="center" justify="center">
            <v-col cols="12" sm="8" md="4" lg="4">
              <v-card class="elevation-4 rounded-xl pa-4 my-2">
                <v-card-title class="text-center text-h4 font-weight-bold mb-2" style="color: rgb(var(--v-primary));">
                  Cadastre-se
                </v-card-title>
                <v-card-text>
                  <v-form @submit.prevent="register">
                    <v-text-field v-model="newUser.full_name" label="Nome de Usuário" prepend-inner-icon="mdi-account"
                      variant="outlined" :rules="userRules" class="mb-2"></v-text-field>

                    <v-text-field v-model="newUser.name" label="Nome Completo" prepend-inner-icon="mdi-account-outline"
                      variant="outlined" :rules="nameRules" class="mb-2"></v-text-field>

                    <v-text-field v-model="newUser.email" label="E-mail" prepend-inner-icon="mdi-email-outline"
                      variant="outlined" :rules="emailRules" class="mb-2"></v-text-field>

                    <v-text-field v-model="newUser.password" label="Senha" :type="showPassword ? 'text' : 'password'"
                      prepend-inner-icon="mdi-lock-outline"
                      :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                      @click:append-inner="showPassword = !showPassword" variant="outlined" :rules="passwordRules"
                      @input="checkPasswordStrength" class="mb-2"></v-text-field>

                    <v-row class="mb-4 px-3">
                      <v-col v-for="(item, i) in passwordStrength" :key="i" class="pa-1">
                        <v-progress-linear :model-value="item.value" :color="item.color" height="5"
                          rounded></v-progress-linear>
                      </v-col>
                    </v-row>

                    <v-btn type="submit" color="primary" block size="large" class="mb-6">
                      REGISTRAR
                    </v-btn>

                    <!-- <v-divider class="my-4">
                      <span class="text-caption">OU</span>
                    </v-divider> -->

                    <!-- <v-row>
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
                    </v-row> -->

                    <div class="mt-6 text-center">
                      <span>Já tem uma conta?</span>
                      <router-link to="/login" class="ml-1 text-primary font-weight-bold">Acesse</router-link>
                    </div>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-container></v-img>
    </v-main>
  </v-app>
</template>

<script setup>
  import { ref, reactive } from 'vue';

  const newUser = ref({
    name: "",
    email: "",
    password: ""
  });

  const showPassword = ref(false);

  const userRules = [
    v => !!v || 'O usuário é obrigatório',
  ];

  const nameRules = [
    v => !!v || 'O nome é obrigatório',
  ];

  const emailRules = [
    v => !!v || 'O e-mail é obrigatório',
    v => /.+@.+\..+/.test(v) || 'O e-mail deve ser válido',
  ];

  const passwordRules = [
    v => !!v || 'A senha é obrigatória',
    v => (v && v.length >= 8) || 'A senha deve ter no mínimo 8 caracteres',
    v => /[A-Z]/.test(v) || 'A senha deve conter pelo menos uma letra maiúscula',
    v => /[a-z]/.test(v) || 'A senha deve conter pelo menos uma letra minúscula',
    v => /[0-9]/.test(v) || 'A senha deve conter pelo menos um número',
    v => /[!@#$%^&*(),.?":{}|<>]/.test(v) || 'A senha deve conter pelo menos um caractere especial'
  ];

  const passwordStrength = reactive([
    { value: 0, color: 'grey' },
    { value: 0, color: 'grey' },
    { value: 0, color: 'grey' },
    { value: 0, color: 'grey' }
  ]);

  const checkPasswordStrength = () => {
    const p = newUser.value.password;
    const checks = [
      p.length >= 8,
      /[A-Z]/.test(p) && /[a-z]/.test(p),
      /[0-9]/.test(p),
      /[!@#$%^&*(),.?":{}|<>]/.test(p)
    ];

    let strength = 0;
    checks.forEach(check => {
      if (check) strength++;
    });

    for (let i = 0; i < 4; i++) {
      if (i < strength) {
        passwordStrength[i].value = 100;
        if (strength === 1) passwordStrength[i].color = 'red';
        else if (strength === 2) passwordStrength[i].color = 'orange';
        else if (strength === 3) passwordStrength[i].color = 'yellow';
        else passwordStrength[i].color = 'green';
      } else {
        passwordStrength[i].value = 0;
        passwordStrength[i].color = 'grey';
      }
    }
  };

  const register = () => {
    // Lógica de registro aqui
    console.log("Dados do novo usuário:", newUser.value);
  };
</script>

<style scoped>
  .v-card-title {
    color: #1976D2;
    /* Cor primária do Vuetify */
  }

  .text-primary {
    color: #1976D2 !important;
  }
</style>