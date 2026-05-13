<template>
  <div>

    <!-- ═══════════════════════════════════════════
         VISITANTE: landing institucional
    ════════════════════════════════════════════ -->
    <template v-if="!authStore.user">
      <v-img
        src="/igreja.jpg"
        height="100vh"
        cover
        gradient="to right, rgba(10,20,60,0.85) 0%, rgba(0,0,0,0.5) 100%"
        class="d-flex align-center"
      >
        <v-container>
          <v-row justify="center">
            <v-col cols="12" md="8" lg="7" class="text-center text-white">
              <v-img src="/laudato.png" height="80" width="80" class="mx-auto mb-6" />
              <h1 class="text-h3 text-sm-h2 font-weight-bold mb-4 hero-title">
                Plataforma de Gestão Paroquial Católica
              </h1>
              <p class="text-h6 font-weight-light opacity-80 mb-10">
                Uma solução unificada para administração simplificada e engajamento comunitário vibrante.
              </p>

              <v-card class="parish-selector mx-auto" max-width="720" rounded="xl" elevation="8">
                <v-card-text class="pa-5">
                  <p class="text-body-1 font-weight-medium text-grey-darken-2 mb-3">
                    <v-icon class="mr-1" size="18">mdi-church</v-icon>
                    Encontre sua paróquia
                  </p>
                  <v-autocomplete
                    v-model="selectedSlug"
                    :items="parishes"
                    item-title="name"
                    item-value="slug"
                    placeholder="Buscar paróquia pelo nome..."
                    variant="outlined"
                    density="comfortable"
                    hide-details
                    rounded="lg"
                    :loading="loadingParishes"
                    no-data-text="Nenhuma paróquia encontrada"
                    clearable
                    @update:model-value="goToParish"
                  >
                    <template #item="{ item, props }">
                      <v-list-item v-bind="props" :subtitle="item.raw.diocese_name || item.raw.address || item.raw.slug">
                        <template #prepend>
                          <v-avatar color="primary" variant="tonal" size="36" class="mr-2">
                            <v-icon size="18">mdi-church</v-icon>
                          </v-avatar>
                        </template>
                      </v-list-item>
                    </template>
                  </v-autocomplete>
                  <div class="d-flex ga-2 mt-3">
                    <v-btn to="/login" variant="tonal" color="primary" size="small" block class="text-none">Entrar</v-btn>
                    <v-btn to="/register-parish" variant="outlined" color="primary" size="small" block class="text-none">Cadastrar paróquia</v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-img>

      <!-- Features -->
      <div class="bg-white py-16" id="features">
        <v-container>
          <div class="text-center mb-12">
            <h2 class="text-h4 font-weight-bold text-grey-darken-3">Tudo que sua paróquia precisa</h2>
            <p class="text-body-1 text-grey mt-2">Módulos integrados para cada área da gestão paroquial</p>
          </div>
          <v-row justify="center">
            <v-col v-for="f in features" :key="f.title" cols="12" sm="6" md="4" class="d-flex">
              <v-card variant="flat" class="feature-card fill-height text-center pa-6 rounded-xl" width="100%">
                <v-avatar :color="f.color" variant="tonal" size="64" class="mb-4">
                  <v-icon :icon="f.icon" size="28" />
                </v-avatar>
                <h3 class="text-subtitle-1 font-weight-bold mb-2">{{ f.title }}</h3>
                <p class="text-body-2 text-grey-darken-1">{{ f.desc }}</p>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </div>

      <div class="cta-section py-16">
        <v-container>
          <v-row align="center" justify="center">
            <v-col cols="12" md="6" class="text-center text-white">
              <h2 class="text-h4 font-weight-bold mb-4">Sua paróquia ainda não está aqui?</h2>
              <p class="text-body-1 opacity-80 mb-8">Cadastre gratuitamente e comece a organizar sua comunidade hoje.</p>
              <v-btn to="/register-parish" color="white" size="x-large" rounded="pill" class="text-primary font-weight-bold px-10">
                Cadastrar paróquia
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </div>
    </template>

    <!-- ═══════════════════════════════════════════
         LOGADO: dashboard da paróquia
    ════════════════════════════════════════════ -->
    <template v-else>
      <!-- Header de boas-vindas -->
      <div class="dashboard-header">
        <v-container class="py-6">
          <v-row align="center" justify="space-between">
            <v-col cols="12" sm="auto">
              <p class="text-caption text-white opacity-60 mb-1">Bem-vindo de volta</p>
              <h1 class="text-h5 font-weight-bold text-white">
                {{ authStore.user.full_name || authStore.user.username }}
              </h1>
            </v-col>
            <v-col cols="12" sm="auto">
              <!-- Seletor de paróquia para visualização -->
              <v-autocomplete
                v-model="viewSlug"
                :items="parishes"
                item-title="name"
                item-value="slug"
                variant="outlined"
                density="compact"
                hide-details
                rounded="lg"
                :loading="loadingParishes"
                no-data-text="Nenhuma paróquia encontrada"
                class="parish-switcher"
                @update:model-value="loadDashboard"
              >
                <template #prepend-inner>
                  <v-icon size="16" class="mr-1">mdi-church</v-icon>
                </template>
                <template #item="{ item, props }">
                  <v-list-item v-bind="props" :subtitle="item.raw.diocese_name || item.raw.address || item.raw.slug" />
                </template>
              </v-autocomplete>
            </v-col>
          </v-row>
        </v-container>
      </div>

      <v-container class="py-8">

        <!-- Linha 1: Avisos + Próximas Missas -->
        <v-row class="mb-6">

          <!-- Avisos -->
          <v-col cols="12" md="7">
            <div class="section-title mb-4">
              <v-icon color="primary" class="mr-2">mdi-bullhorn-outline</v-icon>
              <span class="text-subtitle-1 font-weight-bold">Avisos</span>
            </div>

            <v-progress-linear v-if="loadingNotices" indeterminate color="primary" class="mb-4" rounded />

            <template v-else-if="notices.length">
              <v-card
                v-for="n in notices"
                :key="n.id"
                class="mb-3"
                rounded="lg"
                variant="outlined"
              >
                <v-card-item>
                  <template #prepend>
                    <v-avatar :color="n.color || 'primary'" variant="tonal" size="38" class="mr-3">
                      <v-icon size="18">{{ n.icon || 'mdi-bell-outline' }}</v-icon>
                    </v-avatar>
                  </template>
                  <v-card-title class="text-body-1 font-weight-bold">{{ n.title }}</v-card-title>
                  <v-card-subtitle class="d-flex flex-wrap align-center ga-1 mt-1">
                    <v-chip v-if="n.community_name" size="x-small" color="secondary" variant="tonal" prepend-icon="mdi-map-marker-outline">
                      {{ n.community_name }}
                    </v-chip>
                    <span v-if="n.event_date" class="text-caption text-grey-darken-1">
                      {{ formatDate(n.event_date) }}
                    </span>
                  </v-card-subtitle>
                </v-card-item>
                <v-card-text class="text-body-2 pt-0">{{ n.content }}</v-card-text>
              </v-card>
            </template>

            <v-card v-else variant="flat" class="empty-state text-center pa-8" rounded="lg">
              <v-icon size="40" color="grey-lighten-2">mdi-bell-off-outline</v-icon>
              <p class="text-body-2 text-grey mt-3">Nenhum aviso no momento.</p>
            </v-card>
          </v-col>

          <!-- Próximas Missas -->
          <v-col cols="12" md="5">
            <div class="section-title mb-4">
              <v-icon color="primary" class="mr-2">mdi-calendar-clock</v-icon>
              <span class="text-subtitle-1 font-weight-bold">Próximas Missas</span>
            </div>

            <v-progress-linear v-if="loadingCelebrations" indeterminate color="primary" class="mb-4" rounded />

            <template v-else-if="celebrations.length">
              <v-card
                v-for="cel in celebrations"
                :key="cel.id"
                class="mb-3"
                rounded="lg"
                color="primary"
                variant="tonal"
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
                    <span v-if="cel.description" class="font-weight-regular text-body-2"> — {{ cel.description }}</span>
                  </v-card-title>
                  <v-card-subtitle v-if="cel.assignments.length" class="text-caption">
                    {{ cel.assignments.map(a => `${a.role_name}: ${a.user_name}`).join(' · ') }}
                  </v-card-subtitle>
                </v-card-item>
              </v-card>
            </template>

            <v-card v-else variant="flat" class="empty-state text-center pa-8" rounded="lg">
              <v-icon size="40" color="grey-lighten-2">mdi-calendar-blank-outline</v-icon>
              <p class="text-body-2 text-grey mt-3">Nenhuma missa agendada.</p>
            </v-card>
          </v-col>
        </v-row>

        <v-divider class="mb-6" />

        <!-- Linha 2: Velas Virtuais + Intenções de Missa -->
        <v-row>

          <!-- Velas Virtuais -->
          <v-col cols="12" md="6">
            <div class="section-title mb-4">
              <v-icon color="orange" class="mr-2">mdi-candle</v-icon>
              <span class="text-subtitle-1 font-weight-bold">Velas Virtuais</span>
            </div>

            <v-card rounded="lg" variant="outlined" class="pa-2">
              <!-- Velas acesas (placeholder) -->
              <v-card-text>
                <div v-if="candles.length" class="candles-grid">
                  <div v-for="c in candles" :key="c.id" class="candle-item">
                    <v-icon color="orange" size="32">mdi-candle</v-icon>
                    <p class="text-caption text-center mt-1">{{ c.intention }}</p>
                    <p class="text-caption text-grey text-center">{{ c.author }}</p>
                  </div>
                </div>
                <div v-else class="text-center py-6">
                  <v-icon size="48" color="orange-lighten-3">mdi-candle</v-icon>
                  <p class="text-body-2 text-grey mt-3">Nenhuma vela acesa ainda.</p>
                </div>
              </v-card-text>
              <v-card-actions class="justify-center pb-4">
                <v-btn color="orange" variant="tonal" rounded="pill" prepend-icon="mdi-plus" to="/devotional">
                  Acender uma vela
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>

          <!-- Intenções de Missa -->
          <v-col cols="12" md="6">
            <div class="section-title mb-4">
              <v-icon color="purple" class="mr-2">mdi-hands-pray</v-icon>
              <span class="text-subtitle-1 font-weight-bold">Intenções de Missa</span>
            </div>

            <v-card rounded="lg" variant="outlined">
              <v-list v-if="intentions.length" lines="two" density="compact">
                <v-list-item
                  v-for="intent in intentions"
                  :key="intent.id"
                  :title="intent.description"
                  :subtitle="`${intent.author} · ${formatDate(intent.created_at)}`"
                  prepend-icon="mdi-hands-pray"
                >
                  <template #prepend>
                    <v-icon color="purple" class="mr-2">mdi-hands-pray</v-icon>
                  </template>
                </v-list-item>
              </v-list>
              <div v-else class="text-center py-8">
                <v-icon size="48" color="purple-lighten-3">mdi-hands-pray</v-icon>
                <p class="text-body-2 text-grey mt-3">Nenhuma intenção enviada ainda.</p>
              </div>
              <v-card-actions class="justify-center pb-4">
                <v-btn color="purple" variant="tonal" rounded="pill" prepend-icon="mdi-plus" to="/devotional">
                  Enviar intenção
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>

        </v-row>
      </v-container>
    </template>

  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/useAuthStore.js';

const router = useRouter();
const authStore = useAuthStore();

// ── Visitante ──────────────────────────────────
const parishes    = ref([]);
const loadingParishes = ref(false);
const selectedSlug = ref(null);

const fetchParishes = async () => {
  loadingParishes.value = true;
  try {
    const { data } = await asyncUseApi('/parish/', { server: false });
    parishes.value = data.value ?? [];
  } catch (e) {
    console.error(e);
  } finally {
    loadingParishes.value = false;
  }
};

const goToParish = (slug) => { if (slug) router.push(`/${slug}`); };

// ── Logado ──────────────────────────────────────
const viewSlug          = ref(null);   // paróquia sendo visualizada (pode ser outra)
const notices           = ref([]);
const celebrations      = ref([]);
const candles           = ref([]);     // futuro: /devotional/candles/
const intentions        = ref([]);     // futuro: /devotional/intentions/
const loadingNotices      = ref(false);
const loadingCelebrations = ref(false);

const loadDashboard = async (slug) => {
  if (!slug) return;
  loadNotices(slug);
  loadCelebrations(slug);
  // candles e intentions: aguardam implementação do módulo devocional
};

const loadNotices = async (slug) => {
  loadingNotices.value = true;
  try {
    const [{ data: wData }, { data: cData }, { data: commData }] = await Promise.all([
      asyncUseApi(`/warnings/?parish_slug=${slug}`, { server: false }),
      asyncUseApi(`/category/?parish_slug=${slug}`, { server: false }),
      asyncUseApi(`/community/?type=comunidade`, { server: false }),
    ]);
    const catMap  = Object.fromEntries((cData.value ?? []).map(c => [c.id, c]));
    const commMap = Object.fromEntries((commData.value ?? []).map(c => [c.id, c.name]));
    notices.value = (wData.value ?? []).map(w => ({
      ...w,
      icon:           catMap[w.category_id]?.icon  || 'mdi-bell-outline',
      color:          catMap[w.category_id]?.color || 'primary',
      community_name: w.community_id ? (commMap[w.community_id] ?? null) : null,
    }));
  } catch (e) { console.error(e); }
  finally { loadingNotices.value = false; }
};

const loadCelebrations = async (slug) => {
  loadingCelebrations.value = true;
  try {
    const { data } = await asyncUseApi(`/celebration/public?parish_slug=${slug}`, { server: false });
    celebrations.value = data.value ?? [];
  } catch (e) { console.error(e); }
  finally { loadingCelebrations.value = false; }
};

// ── Helpers de data ─────────────────────────────
const formatDate = (d) => d ? new Date(d).toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' }) : '';
const celDay   = (d) => new Date(d).getDate().toString().padStart(2, '0');
const celMonth = (d) => new Date(d).toLocaleDateString('pt-BR', { month: 'short' }).replace('.', '');
const celTime  = (d) => new Date(d).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

// ── Features (landing) ───────────────────────────
const features = [
  { icon: 'mdi-calendar-check', color: 'teal',   title: 'Escalas e Missas',    desc: 'Organize celebrações, designe leitores, ministros e músicos.' },
  { icon: 'mdi-bell-outline',   color: 'blue',   title: 'Avisos e Comunicados', desc: 'Publique avisos e eventos para toda a comunidade em tempo real.' },
  { icon: 'mdi-church',         color: 'purple', title: 'Sacramentos',          desc: 'Registre batismos, crismas, matrimônios e demais sacramentos.' },
  { icon: 'mdi-account-group',  color: 'green',  title: 'Gestão de Membros',    desc: 'Cadastre paroquianos, atribua funções e gerencie permissões.' },
  { icon: 'mdi-cash-multiple',  color: 'amber',  title: 'Financeiro',           desc: 'Controle dízimos, campanhas e doações com relatórios.' },
  { icon: 'mdi-candle',         color: 'orange', title: 'Devocional',           desc: 'Intenções de missa, velas virtuais e biblioteca de orações.' },
];

onMounted(async () => {
  await fetchParishes();
  if (authStore.user && authStore.parishSlug) {
    viewSlug.value = authStore.parishSlug;
    loadDashboard(authStore.parishSlug);
  }
});
</script>

<style scoped>
/* ── Landing ── */
.hero-title { line-height: 1.2; text-shadow: 0 2px 12px rgba(0,0,0,0.3); }
.parish-selector { backdrop-filter: blur(8px); background: rgba(255,255,255,0.97) !important; }

.feature-card {
  border: 1px solid #f0f0f0;
  transition: box-shadow 0.2s, transform 0.2s;
}
.feature-card:hover {
  box-shadow: 0 8px 32px rgba(0,0,0,0.08) !important;
  transform: translateY(-4px);
}
.cta-section {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, #1a237e 100%);
}

/* ── Dashboard ── */
.dashboard-header {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, #1a237e 100%);
}

.parish-switcher {
  min-width: 260px;
  background: rgba(255, 255, 255, 0.12);
  border-radius: 10px;
}

.parish-switcher :deep(.v-field) {
  background: rgba(255, 255, 255, 0.12) !important;
  border: 1.5px solid rgba(255, 255, 255, 0.45) !important;
  border-radius: 10px !important;
  color: white !important;
}

.parish-switcher :deep(.v-field:hover) {
  border-color: rgba(255, 255, 255, 0.75) !important;
}

.parish-switcher :deep(.v-field__input),
.parish-switcher :deep(.v-field__prepend-inner .v-icon),
.parish-switcher :deep(.v-field__append-inner .v-icon) {
  color: white !important;
  opacity: 1 !important;
}

.parish-switcher :deep(.v-field__outline) {
  display: none;
}

.section-title {
  display: flex;
  align-items: center;
}

.empty-state {
  background: #fafafa;
  border: 1.5px dashed #e0e0e0 !important;
}

.date-badge {
  background: rgb(var(--v-theme-primary));
  color: white;
  border-radius: 8px;
  padding: 4px 10px;
  text-align: center;
  min-width: 44px;
}
.date-day   { font-size: 18px; font-weight: 700; line-height: 1.1; }
.date-month { font-size: 10px; text-transform: uppercase; opacity: 0.85; }

.candles-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
  padding: 8px 0;
}
.candle-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 72px;
}
</style>
