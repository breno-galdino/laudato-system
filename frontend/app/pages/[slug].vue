<template>
  <div>
    <!-- 404 -->
    <div v-if="notFound" class="text-center py-24">
      <v-icon size="80" color="grey-lighten-2">mdi-church</v-icon>
      <h2 class="text-h5 text-grey-darken-1 mt-4">Paróquia não encontrada</h2>
      <p class="text-body-2 text-grey mt-2">O endereço <strong>{{ slug }}</strong> não corresponde a nenhuma paróquia cadastrada.</p>
      <v-btn to="/" color="primary" class="mt-6" rounded="pill">Voltar ao início</v-btn>
    </div>

    <template v-else-if="parish">
      <!-- Header da paróquia -->
      <div class="parish-hero">
        <v-container class="py-12">
          <v-row align="center" justify="center">
            <v-col cols="12" md="8" class="text-center text-white">
              <v-avatar color="white" size="80" class="mb-4 elevation-4">
                <v-icon size="40" color="primary">mdi-church</v-icon>
              </v-avatar>
              <h1 class="text-h4 font-weight-bold mb-2">{{ parish.name }}</h1>
              <div class="d-flex flex-wrap justify-center ga-3 mt-3 opacity-90">
                <span v-if="parish.address" class="d-flex align-center text-body-2">
                  <v-icon size="16" class="mr-1">mdi-map-marker</v-icon>{{ parish.address }}
                </span>
                <span v-if="parish.email" class="d-flex align-center text-body-2">
                  <v-icon size="16" class="mr-1">mdi-email</v-icon>{{ parish.email }}
                </span>
                <span v-if="parish.phone" class="d-flex align-center text-body-2">
                  <v-icon size="16" class="mr-1">mdi-phone</v-icon>{{ parish.phone }}
                </span>
              </div>
              <div v-if="!authStore.user" class="d-flex justify-center ga-3 mt-6">
                <v-btn :to="`/register?parish=${slug}`" color="white" variant="elevated" rounded="pill" class="text-primary font-weight-bold px-6">
                  <v-icon start>mdi-account-plus</v-icon>
                  Quero participar
                </v-btn>
                <v-btn to="/login" variant="outlined" color="white" rounded="pill" class="px-6">
                  Entrar
                </v-btn>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </div>

      <v-container class="py-10">
        <v-row>

          <!-- Avisos -->
          <v-col cols="12" md="7">
            <div class="d-flex align-center mb-5">
              <v-icon color="primary" class="mr-2">mdi-bullhorn-outline</v-icon>
              <h2 class="text-h6 font-weight-bold">Avisos e Eventos</h2>
            </div>

            <div v-if="loadingNotices" class="d-flex justify-center py-8">
              <v-progress-circular indeterminate color="primary" />
            </div>

            <template v-else-if="notices.length > 0">
              <v-card
                v-for="notice in notices"
                :key="notice.id"
                class="mb-3 notice-card"
                rounded="lg"
                variant="outlined"
              >
                <v-card-item :prepend-icon="notice.icon">
                  <template #prepend>
                    <v-avatar :color="notice.color || 'primary'" variant="tonal" size="40" class="mr-3">
                      <v-icon size="20">{{ notice.icon || 'mdi-bell-outline' }}</v-icon>
                    </v-avatar>
                  </template>
                  <v-card-title class="text-body-1 font-weight-bold">{{ notice.title }}</v-card-title>
                  <v-card-subtitle v-if="notice.event_date" class="text-caption">
                    {{ formatDate(notice.event_date) }}
                  </v-card-subtitle>
                </v-card-item>
                <v-card-text class="text-body-2 pt-0">{{ notice.content }}</v-card-text>
              </v-card>
            </template>

            <div v-else class="text-center py-10 text-grey">
              <v-icon size="48" color="grey-lighten-2">mdi-bell-off-outline</v-icon>
              <p class="mt-3 text-body-2">Nenhum aviso no momento.</p>
            </div>
          </v-col>

          <!-- Próximas missas -->
          <v-col cols="12" md="5">
            <div class="d-flex align-center mb-5">
              <v-icon color="primary" class="mr-2">mdi-calendar-clock</v-icon>
              <h2 class="text-h6 font-weight-bold">Próximas Missas</h2>
            </div>

            <div v-if="loadingCelebrations" class="d-flex justify-center py-8">
              <v-progress-circular indeterminate color="primary" />
            </div>

            <template v-else-if="celebrations.length > 0">
              <v-card
                v-for="cel in celebrations"
                :key="cel.id"
                class="mb-3 celebration-card"
                rounded="lg"
                variant="tonal"
                color="primary"
              >
                <v-card-item>
                  <template #prepend>
                    <div class="date-badge mr-3">
                      <div class="date-day">{{ celDay(cel.date) }}</div>
                      <div class="date-month">{{ celMonth(cel.date) }}</div>
                    </div>
                  </template>
                  <v-card-title class="text-body-1 font-weight-bold">
                    {{ celTime(cel.date) }}
                    <span v-if="cel.description" class="font-weight-regular text-body-2 ml-1">
                      — {{ cel.description }}
                    </span>
                  </v-card-title>
                  <v-card-subtitle v-if="cel.assignments.length > 0" class="text-caption">
                    {{ cel.assignments.map(a => `${a.role_name}: ${a.user_name}`).join(' · ') }}
                  </v-card-subtitle>
                </v-card-item>
              </v-card>
            </template>

            <div v-else class="text-center py-10 text-grey">
              <v-icon size="48" color="grey-lighten-2">mdi-calendar-blank-outline</v-icon>
              <p class="mt-3 text-body-2">Nenhuma missa agendada.</p>
            </div>
          </v-col>

        </v-row>
      </v-container>
    </template>

    <!-- Loading inicial -->
    <div v-else class="d-flex justify-center align-center" style="min-height: 60vh;">
      <v-progress-circular indeterminate color="primary" size="48" />
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/useAuthStore.js';

const route = useRoute();
const authStore = useAuthStore();
const slug = computed(() => route.params.slug);

const parish = ref(null);
const notFound = ref(false);
const notices = ref([]);
const celebrations = ref([]);
const loadingNotices = ref(false);
const loadingCelebrations = ref(false);

// Carrega info da paróquia
const fetchParish = async () => {
  try {
    const { data, error } = await asyncUseApi(`/parish/${slug.value}`, { server: false });
    if (error.value || !data.value) {
      notFound.value = true;
      return;
    }
    parish.value = data.value;
    fetchNotices();
    fetchCelebrations();
  } catch {
    notFound.value = true;
  }
};

// Avisos públicos
const fetchNotices = async () => {
  loadingNotices.value = true;
  try {
    const [{ data: warningsData }, { data: catsData }] = await Promise.all([
      asyncUseApi(`/warnings/?parish_slug=${slug.value}`, { server: false }),
      asyncUseApi(`/category/?parish_slug=${slug.value}`, { server: false }),
    ]);
    const cats = catsData.value ?? [];
    const catMap = Object.fromEntries(cats.map(c => [c.id, c]));
    notices.value = (warningsData.value ?? []).map(w => ({
      ...w,
      icon: catMap[w.category_id]?.icon || 'mdi-bell-outline',
      color: catMap[w.category_id]?.color || 'primary',
    }));
  } catch (e) {
    console.error(e);
  } finally {
    loadingNotices.value = false;
  }
};

// Celebrações públicas
const fetchCelebrations = async () => {
  loadingCelebrations.value = true;
  try {
    const { data } = await asyncUseApi(`/celebration/public?parish_slug=${slug.value}`, { server: false });
    celebrations.value = data.value ?? [];
  } catch (e) {
    console.error(e);
  } finally {
    loadingCelebrations.value = false;
  }
};

// Formatação de datas
const formatDate = (d) => d ? new Date(d).toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' }) : '';
const celDay = (d) => new Date(d).getDate().toString().padStart(2, '0');
const celMonth = (d) => new Date(d).toLocaleDateString('pt-BR', { month: 'short' }).replace('.', '');
const celTime = (d) => new Date(d).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

// SEO básico
useHead(() => ({
  title: parish.value ? `${parish.value.name} — Laudato System` : 'Carregando...',
}));

onMounted(fetchParish);
</script>

<style scoped>
.parish-hero {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, #1a237e 100%);
  position: relative;
  overflow: hidden;
}

.parish-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/igreja.jpg') center/cover no-repeat;
  opacity: 0.1;
}

.parish-hero > * {
  position: relative;
}

.notice-card {
  transition: box-shadow 0.2s;
}
.notice-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
}

.date-badge {
  background: rgb(var(--v-theme-primary));
  color: white;
  border-radius: 8px;
  padding: 4px 10px;
  text-align: center;
  min-width: 44px;
}
.date-day {
  font-size: 20px;
  font-weight: 700;
  line-height: 1.1;
}
.date-month {
  font-size: 11px;
  text-transform: uppercase;
  opacity: 0.85;
}
</style>
