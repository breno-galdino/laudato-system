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
                    <v-text-field
                      v-model="newUser.username"
                      label="Nome de usuário"
                      prepend-inner-icon="mdi-account"
                      variant="outlined"
                      :rules="[v => !!v || 'Obrigatório']"
                      class="mb-2"
                    />

                    <v-text-field
                      v-model="newUser.full_name"
                      label="Nome completo"
                      prepend-inner-icon="mdi-account-outline"
                      variant="outlined"
                      class="mb-2"
                    />

                    <v-text-field
                      v-model="newUser.email"
                      label="E-mail"
                      prepend-inner-icon="mdi-email-outline"
                      variant="outlined"
                      :rules="emailRules"
                      class="mb-2"
                    />

                    <v-autocomplete
                      v-model="newUser.parish_slug"
                      :items="parishes"
                      item-title="name"
                      item-value="slug"
                      label="Paróquia"
                      prepend-inner-icon="mdi-church"
                      variant="outlined"
                      :rules="[v => !!v || 'Obrigatório']"
                      :loading="loadingParishes"
                      no-data-text="Nenhuma paróquia encontrada"
                      class="mb-2"
                    />

                    <v-text-field
                      v-model="newUser.password"
                      label="Senha"
                      :type="showPassword ? 'text' : 'password'"
                      prepend-inner-icon="mdi-lock-outline"
                      :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                      @click:append-inner="showPassword = !showPassword"
                      variant="outlined"
                      :rules="passwordRules"
                      @input="checkPasswordStrength"
                      class="mb-2"
                    />

                    <v-row class="mb-4 px-3">
                      <v-col v-for="(item, i) in passwordStrength" :key="i" class="pa-1">
                        <v-progress-linear :model-value="item.value" :color="item.color" height="5" rounded />
                      </v-col>
                    </v-row>

                    <v-alert v-if="errorMsg" type="error" variant="tonal" class="mb-4" density="compact">
                      {{ errorMsg }}
                    </v-alert>

                    <v-btn type="submit" color="primary" block size="large" class="mb-4" :loading="loading">
                      REGISTRAR
                    </v-btn>

                    <div class="mt-2 text-center">
                      <span>Já tem uma conta?</span>
                      <router-link to="/login" class="ml-1 text-primary font-weight-bold">Acesse</router-link>
                    </div>
                    <div class="mt-2 text-center text-body-2">
                      <span class="text-grey">É uma paróquia?</span>
                      <router-link to="/register-parish" class="ml-1 text-primary font-weight-bold">Cadastre aqui</router-link>
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
import { ref, reactive } from 'vue';

const router = useRouter();
const loading = ref(false);
const loadingParishes = ref(false);
const errorMsg = ref('');
const showPassword = ref(false);
const parishes = ref([]);

const fetchParishes = async () => {
  loadingParishes.value = true;
  try {
    const { data } = await asyncUseApi('/parish/', { server: false });
    parishes.value = data.value ?? [];
  } catch (e) {
    console.error('Erro ao carregar paróquias:', e);
  } finally {
    loadingParishes.value = false;
  }
};

onMounted(fetchParishes);

const newUser = ref({
  username: '',
  full_name: '',
  email: '',
  password: '',
  parish_slug: '',
});

const emailRules = [
  v => !!v || 'O e-mail é obrigatório',
  v => /.+@.+\..+/.test(v) || 'E-mail inválido',
];

const passwordRules = [
  v => !!v || 'A senha é obrigatória',
  v => (v && v.length >= 8) || 'Mínimo 8 caracteres',
  v => /[A-Z]/.test(v) || 'Pelo menos uma letra maiúscula',
  v => /[0-9]/.test(v) || 'Pelo menos um número',
];

const passwordStrength = reactive([
  { value: 0, color: 'grey' },
  { value: 0, color: 'grey' },
  { value: 0, color: 'grey' },
  { value: 0, color: 'grey' },
]);

const checkPasswordStrength = () => {
  const p = newUser.value.password;
  const checks = [
    p.length >= 8,
    /[A-Z]/.test(p) && /[a-z]/.test(p),
    /[0-9]/.test(p),
    /[!@#$%^&*(),.?":{}|<>]/.test(p),
  ];
  let strength = checks.filter(Boolean).length;
  const colors = ['red', 'orange', 'yellow', 'green'];
  passwordStrength.forEach((bar, i) => {
    bar.value = i < strength ? 100 : 0;
    bar.color = i < strength ? colors[strength - 1] : 'grey';
  });
};

const register = async () => {
  errorMsg.value = '';
  loading.value = true;
  try {
    const { data, error } = await asyncUseApi('/auth/register', {
      method: 'POST',
      body: newUser.value,
      credentials: 'include',
      server: false,
    });

    if (error.value) {
      errorMsg.value = error.value?.data?.detail || 'Erro ao registrar.';
      return;
    }

    message.success('Conta criada com sucesso! Faça login para continuar.');
    router.push('/login');
  } catch (e) {
    errorMsg.value = 'Erro inesperado. Tente novamente.';
  } finally {
    loading.value = false;
  }
};
</script>
