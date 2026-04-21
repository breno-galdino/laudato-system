<template>
  <v-app>
    <div class="register-parish-page">

      <!-- Coluna esquerda: branding -->
      <div class="brand-panel hidden-sm-and-down">
        <div class="brand-content">
          <v-img src="/laudato.png" height="72" width="72" class="mb-6" />
          <h1 class="text-h4 font-weight-bold text-white mb-3">Laudato System</h1>
          <p class="text-body-1 text-white opacity-80 mb-8">
            A plataforma completa para gestão paroquial católica.
          </p>
          <div class="features">
            <div v-for="f in features" :key="f.text" class="feature-item">
              <v-icon color="white" size="20" class="mr-3">{{ f.icon }}</v-icon>
              <span class="text-white text-body-2">{{ f.text }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Coluna direita: formulário -->
      <div class="form-panel">
        <div class="form-inner">

          <!-- Logo mobile -->
          <div class="d-sm-none text-center mb-6">
            <v-img src="/laudato.png" height="56" width="56" class="mx-auto mb-3" />
            <h2 class="text-h5 font-weight-bold">Laudato System</h2>
          </div>

          <h2 class="text-h5 font-weight-bold mb-1">Cadastrar Paróquia</h2>
          <p class="text-body-2 text-medium-emphasis mb-6">
            Comece gratuitamente — leva menos de 2 minutos.
          </p>

          <!-- Stepper indicador -->
          <div class="stepper-indicator mb-6">
            <div
              v-for="(s, i) in steps"
              :key="i"
              class="step-item"
              :class="{ active: step === i + 1, done: step > i + 1 }"
            >
              <div class="step-circle">
                <v-icon v-if="step > i + 1" size="14">mdi-check</v-icon>
                <span v-else>{{ i + 1 }}</span>
              </div>
              <span class="step-label">{{ s }}</span>
              <div v-if="i < steps.length - 1" class="step-line" :class="{ done: step > i + 1 }" />
            </div>
          </div>

          <!-- PASSO 1: Dados da Paróquia -->
          <Transition name="slide-fade" mode="out-in">
            <div v-if="step === 1" key="step1">
              <v-text-field
                v-model="form.parish.name"
                label="Nome da Paróquia"
                prepend-inner-icon="mdi-church"
                variant="outlined"
                density="comfortable"
                :rules="[required]"
                class="mb-3"
              />

              <v-text-field
                v-model="form.parish.slug"
                label="Identificador único (slug)"
                prepend-inner-icon="mdi-link"
                variant="outlined"
                density="comfortable"
                hint="Usado na URL — ex: sao-pedro-paulo"
                persistent-hint
                :rules="[required, slugRule]"
                class="mb-3"
                @input="formatSlug"
              >
                <template #prepend-inner>
                  <v-icon size="18" class="mr-1">mdi-link</v-icon>
                  <span class="text-caption text-medium-emphasis mr-1">laudato.app/</span>
                </template>
              </v-text-field>

              <v-row>
                <v-col cols="12" sm="6" class="pb-0 pb-sm-3">
                  <v-text-field
                    v-model="form.parish.email"
                    label="E-mail da Paróquia"
                    prepend-inner-icon="mdi-email-outline"
                    variant="outlined"
                    density="comfortable"
                    class="mb-3"
                  />
                </v-col>
                <v-col cols="12" sm="6" class="pb-0 pb-sm-3">
                  <v-text-field
                    v-model="form.parish.phone"
                    label="Telefone"
                    prepend-inner-icon="mdi-phone-outline"
                    variant="outlined"
                    density="comfortable"
                    class="mb-3"
                  />
                </v-col>
              </v-row>

              <v-text-field
                v-model="form.parish.address"
                label="Endereço"
                prepend-inner-icon="mdi-map-marker-outline"
                variant="outlined"
                density="comfortable"
                placeholder="Rua, número, cidade — SP"
                class="mb-4"
              />

              <v-btn
                color="primary" size="large" block rounded="lg"
                @click="nextStep"
              >
                Continuar
                <v-icon end>mdi-arrow-right</v-icon>
              </v-btn>
            </div>
          </Transition>

          <!-- PASSO 2: Administrador -->
          <Transition name="slide-fade" mode="out-in">
            <div v-if="step === 2" key="step2">
              <v-row>
                <v-col cols="12" sm="6" class="pb-0 pb-sm-3">
                  <v-text-field
                    v-model="form.admin_full_name"
                    label="Nome completo"
                    prepend-inner-icon="mdi-account-outline"
                    variant="outlined"
                    density="comfortable"
                    :rules="[required]"
                    class="mb-3"
                  />
                </v-col>
                <v-col cols="12" sm="6" class="pb-0 pb-sm-3">
                  <v-text-field
                    v-model="form.admin_username"
                    label="Nome de usuário"
                    prepend-inner-icon="mdi-at"
                    variant="outlined"
                    density="comfortable"
                    :rules="[required]"
                    class="mb-3"
                  />
                </v-col>
              </v-row>

              <v-text-field
                v-model="form.admin_email"
                label="E-mail do administrador"
                prepend-inner-icon="mdi-email-outline"
                variant="outlined"
                density="comfortable"
                :rules="[required, emailRule]"
                class="mb-3"
              />

              <v-text-field
                v-model="form.admin_password"
                label="Senha"
                :type="showPassword ? 'text' : 'password'"
                prepend-inner-icon="mdi-lock-outline"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showPassword = !showPassword"
                variant="outlined"
                density="comfortable"
                :rules="[required, v => v.length >= 8 || 'Mínimo 8 caracteres']"
                class="mb-2"
              />

              <!-- Barra de força da senha -->
              <v-row class="mb-4 px-1">
                <v-col v-for="(bar, i) in passwordStrength" :key="i" class="pa-1">
                  <v-progress-linear :model-value="bar.value" :color="bar.color" height="4" rounded />
                </v-col>
              </v-row>

              <v-alert v-if="errorMsg" type="error" variant="tonal" density="compact" class="mb-4">
                {{ errorMsg }}
              </v-alert>

              <v-row>
                <v-col cols="5">
                  <v-btn
                    variant="outlined" color="primary" size="large" block rounded="lg"
                    @click="step = 1"
                  >
                    <v-icon start>mdi-arrow-left</v-icon>
                    Voltar
                  </v-btn>
                </v-col>
                <v-col cols="7">
                  <v-btn
                    color="primary" size="large" block rounded="lg"
                    :loading="loading" @click="submit"
                  >
                    Criar Paróquia
                  </v-btn>
                </v-col>
              </v-row>
            </div>
          </Transition>

          <v-divider class="my-5" />
          <p class="text-center text-body-2 text-medium-emphasis">
            Já tem uma conta?
            <nuxt-link to="/login" class="text-primary font-weight-medium">Entrar</nuxt-link>
            &nbsp;·&nbsp;
            <nuxt-link to="/register" class="text-primary font-weight-medium">Cadastrar usuário</nuxt-link>
          </p>
        </div>
      </div>

    </div>
  </v-app>
</template>

<script setup>
definePageMeta({ layout: false })

const router = useRouter()
const loading = ref(false)
const step = ref(1)
const showPassword = ref(false)
const errorMsg = ref('')

const steps = ['Paróquia', 'Administrador']

const features = [
  { icon: 'mdi-calendar-check', text: 'Escalas e missas organizadas' },
  { icon: 'mdi-account-group', text: 'Gestão de usuários e paroquianos' },
  { icon: 'mdi-bell-outline', text: 'Avisos e comunicados em tempo real' },
  { icon: 'mdi-church', text: 'Registro de sacramentos' },
  { icon: 'mdi-cash-multiple', text: 'Controle financeiro e dízimos' },
]

const form = ref({
  parish: { name: '', slug: '', email: '', phone: '', address: '' },
  admin_full_name: '',
  admin_username: '',
  admin_email: '',
  admin_password: '',
})

const required = v => !!v || 'Campo obrigatório'
const emailRule = v => /.+@.+\..+/.test(v) || 'E-mail inválido'
const slugRule = v => /^[a-z0-9-]+$/.test(v) || 'Use apenas letras minúsculas, números e hífens'

const formatSlug = () => {
  form.value.parish.slug = form.value.parish.slug
    .toLowerCase()
    .replace(/[^a-z0-9-]/g, '-')
    .replace(/-+/g, '-')
}

// Auto-gera slug a partir do nome
watch(() => form.value.parish.name, (val) => {
  if (!form.value.parish.slug || form.value.parish.slug === slugify(form.value.parish.name.slice(0, -1))) {
    form.value.parish.slug = slugify(val)
  }
})

const slugify = (val) =>
  val.toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')

// Barra de força da senha
const passwordStrength = reactive([
  { value: 0, color: 'grey' },
  { value: 0, color: 'grey' },
  { value: 0, color: 'grey' },
  { value: 0, color: 'grey' },
])

watch(() => form.value.admin_password, (p) => {
  const checks = [
    p.length >= 8,
    /[A-Z]/.test(p) && /[a-z]/.test(p),
    /[0-9]/.test(p),
    /[!@#$%^&*(),.?":{}|<>]/.test(p),
  ]
  const strength = checks.filter(Boolean).length
  const colors = ['red', 'orange', 'yellow', 'green']
  passwordStrength.forEach((bar, i) => {
    bar.value = i < strength ? 100 : 0
    bar.color = i < strength ? colors[strength - 1] : 'grey'
  })
})

const nextStep = () => {
  if (!form.value.parish.name || !form.value.parish.slug) {
    message.warning('Preencha o nome e o slug da paróquia.')
    return
  }
  step.value = 2
}

const submit = async () => {
  errorMsg.value = ''
  if (!form.value.admin_email || !form.value.admin_password || !form.value.admin_username) {
    message.warning('Preencha todos os campos obrigatórios.')
    return
  }
  loading.value = true
  try {
    const { data, error } = await asyncUseApi('/parish/register', {
      method: 'POST',
      body: form.value,
    })
    if (error.value) {
      errorMsg.value = error.value?.data?.detail || 'Erro ao cadastrar paróquia.'
      return
    }
    message.success(`Paróquia "${data.value.parish.name}" criada! Faça login para continuar.`)
    await router.push('/login')
  } catch (e) {
    errorMsg.value = 'Erro inesperado. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-parish-page {
  display: flex;
  min-height: 100vh;
}

/* ── Painel esquerdo ── */
.brand-panel {
  width: 420px;
  min-width: 360px;
  background: linear-gradient(160deg, rgb(var(--v-theme-primary)) 0%, #1a237e 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 40px;
  position: relative;
  overflow: hidden;
}

.brand-panel::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/igreja.jpg') center/cover no-repeat;
  opacity: 0.08;
}

.brand-content {
  position: relative;
  z-index: 1;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feature-item {
  display: flex;
  align-items: center;
  padding: 10px 14px;
  background: rgba(255,255,255,0.1);
  border-radius: 10px;
  backdrop-filter: blur(4px);
}

/* ── Painel direito ── */
.form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7f8fa;
  padding: 32px 16px;
}

.form-inner {
  width: 100%;
  max-width: 480px;
  background: #fff;
  border-radius: 20px;
  padding: 40px 36px;
  box-shadow: 0 4px 32px rgba(0,0,0,0.07);
}

/* ── Stepper ── */
.stepper-indicator {
  display: flex;
  align-items: center;
  gap: 0;
}

.step-item {
  display: flex;
  align-items: center;
  flex: 1;
  gap: 8px;
}

.step-circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
  background: #e0e0e0;
  color: #9e9e9e;
  transition: all 0.3s ease;
}

.step-item.active .step-circle {
  background: rgb(var(--v-theme-primary));
  color: #fff;
  box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.4);
}

.step-item.done .step-circle {
  background: rgb(var(--v-theme-primary));
  color: #fff;
}

.step-label {
  font-size: 12px;
  font-weight: 600;
  color: #9e9e9e;
  transition: color 0.3s;
  white-space: nowrap;
}

.step-item.active .step-label,
.step-item.done .step-label {
  color: rgb(var(--v-theme-primary));
}

.step-line {
  flex: 1;
  height: 2px;
  background: #e0e0e0;
  margin: 0 8px;
  border-radius: 2px;
  transition: background 0.3s;
}

.step-line.done {
  background: rgb(var(--v-theme-primary));
}

/* ── Transição de passo ── */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.25s ease;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(24px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-24px);
}

@media (max-width: 599px) {
  .form-inner {
    padding: 28px 20px;
    border-radius: 16px;
  }
}
</style>
