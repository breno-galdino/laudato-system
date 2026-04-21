<template>
  <v-container class="py-8" max-width="1000">

    <!-- Header -->
    <div class="d-flex align-center justify-space-between mb-6 flex-wrap ga-3">
      <div>
        <h1 class="text-h5 font-weight-bold">Comunidade</h1>
        <p class="text-body-2 text-medium-emphasis mt-1">
          {{ authStore.parish?.name }}
        </p>
      </div>
      <v-btn
        v-if="authStore.canManage"
        variant="tonal"
        prepend-icon="mdi-cog-outline"
        class="text-none"
        to="/management/community"
        size="small"
      >
        Gerenciar
      </v-btn>
    </div>

    <!-- Tabs -->
    <v-tabs v-model="tab" color="primary" class="mb-6">
      <v-tab value="comunidade" class="text-none">
        <v-icon start size="18">mdi-church</v-icon>
        Comunidades
        <v-chip v-if="comunidades.length" size="x-small" class="ml-2">{{ comunidades.length }}</v-chip>
      </v-tab>
      <v-tab value="grupo" class="text-none">
        <v-icon start size="18">mdi-account-group</v-icon>
        Grupos
        <v-chip v-if="grupos.length" size="x-small" class="ml-2">{{ grupos.length }}</v-chip>
      </v-tab>
      <v-tab value="pastoral" class="text-none">
        <v-icon start size="18">mdi-hands-pray</v-icon>
        Pastorais
        <v-chip v-if="pastorais.length" size="x-small" class="ml-2">{{ pastorais.length }}</v-chip>
      </v-tab>
    </v-tabs>

    <!-- Loading -->
    <div v-if="loading" class="d-flex justify-center py-12">
      <v-progress-circular indeterminate color="primary" />
    </div>

    <!-- Empty state -->
    <div
      v-else-if="currentList.length === 0"
      class="d-flex flex-column align-center py-16 text-medium-emphasis"
    >
      <v-icon size="56" class="mb-4 opacity-30">{{ TAB_META[tab].icon }}</v-icon>
      <p class="text-body-1">
        Nenhum{{ TAB_META[tab].feminin ? 'a' : '' }}
        {{ TAB_META[tab].label.toLowerCase() }}
        cadastrad{{ TAB_META[tab].feminin ? 'a' : 'o' }} ainda.
      </p>
      <v-btn
        v-if="authStore.canManage"
        color="primary"
        variant="tonal"
        class="text-none mt-4"
        to="/management/community"
        prepend-icon="mdi-plus"
      >
        Adicionar
      </v-btn>
    </div>

    <!-- Grid de cards -->
    <v-row v-else>
      <v-col
        v-for="item in currentList"
        :key="item.id"
        cols="12" sm="6" md="4"
      >
        <v-card height="100%" elevation="0" border rounded="lg" class="community-card">
          <v-card-text class="pa-5">
            <!-- Ícone + nome -->
            <div class="d-flex align-start ga-3 mb-3">
              <v-avatar
                :color="TAB_META[tab].color"
                size="44"
                rounded="lg"
                class="flex-shrink-0"
              >
                <v-icon color="white" size="22">{{ TAB_META[tab].icon }}</v-icon>
              </v-avatar>
              <div>
                <p class="text-subtitle-2 font-weight-bold">{{ item.name }}</p>
                <p v-if="item.coordinator" class="text-caption text-medium-emphasis">
                  {{ tab === 'comunidade' ? 'Resp.' : 'Coord.' }}: {{ item.coordinator }}
                </p>
              </div>
            </div>

            <!-- Descrição -->
            <p v-if="item.description" class="text-body-2 text-medium-emphasis mb-3 description-clamp">
              {{ item.description }}
            </p>

            <!-- Endereço (comunidades) -->
            <div v-if="tab === 'comunidade' && item.address" class="d-flex align-center ga-1 text-caption text-medium-emphasis">
              <v-icon size="14">mdi-map-marker-outline</v-icon>
              <span>{{ item.address }}</span>
            </div>

            <!-- Reunião (grupos/pastorais) -->
            <div v-if="tab !== 'comunidade'" class="d-flex flex-column ga-1">
              <div v-if="item.meeting_day" class="d-flex align-center ga-1 text-caption">
                <v-icon size="14" color="primary">mdi-calendar-clock</v-icon>
                <span>{{ formatDay(item.meeting_day) }}<span v-if="item.meeting_time"> às {{ item.meeting_time }}</span></span>
              </div>
              <div v-if="item.address" class="d-flex align-center ga-1 text-caption text-medium-emphasis">
                <v-icon size="14">mdi-map-marker-outline</v-icon>
                <span>{{ item.address }}</span>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<script setup>
import { useAuthStore } from '~/stores/useAuthStore.js';

const authStore = useAuthStore();
const tab = ref('comunidade');

const TAB_META = {
  comunidade: { label: 'Comunidade', icon: 'mdi-church',              color: 'indigo',      feminin: true  },
  grupo:      { label: 'Grupo',      icon: 'mdi-account-group',        color: 'primary',     feminin: false },
  pastoral:   { label: 'Pastoral',   icon: 'mdi-hands-pray',           color: 'deep-purple', feminin: true  },
};

const allCommunities = ref([]);
const loading = ref(true);

const comunidades = computed(() => allCommunities.value.filter(c => c.type === 'comunidade'));
const grupos      = computed(() => allCommunities.value.filter(c => c.type === 'grupo'));
const pastorais   = computed(() => allCommunities.value.filter(c => c.type === 'pastoral'));
const currentList = computed(() => {
  if (tab.value === 'comunidade') return comunidades.value;
  if (tab.value === 'grupo')      return grupos.value;
  return pastorais.value;
});

onMounted(async () => {
  try {
    const { data } = await asyncUseApi('/community/');
    allCommunities.value = data.value || [];
  } finally {
    loading.value = false;
  }
});

const DAYS = {
  segunda: 'Segunda-feira',
  terca:   'Terça-feira',
  quarta:  'Quarta-feira',
  quinta:  'Quinta-feira',
  sexta:   'Sexta-feira',
  sabado:  'Sábado',
  domingo: 'Domingo',
};
const formatDay = (d) => DAYS[d] || d;
</script>

<style scoped>
.community-card {
  transition: box-shadow 0.2s;
}
.community-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
}
.description-clamp {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
