<template>
  <v-container class="py-8" max-width="800">

    <!-- Header do perfil -->
    <v-card class="mb-4 profile-header-card" elevation="0" border>
      <v-card-text class="pa-6">
        <div class="d-flex align-center ga-4 flex-wrap">
          <!-- Avatar com iniciais -->
          <v-avatar size="72" color="primary" class="flex-shrink-0">
            <span class="text-h5 font-weight-bold text-white">{{ initials }}</span>
          </v-avatar>

          <div class="flex-grow-1">
            <div class="d-flex align-center ga-2 flex-wrap">
              <h1 class="text-h5 font-weight-bold">{{ authStore.user?.full_name || authStore.user?.username }}</h1>
              <v-chip
                v-if="authStore.isAdmin"
                color="error" size="x-small" label
              >Admin</v-chip>
              <v-chip
                v-else-if="authStore.isMinister"
                color="warning" size="x-small" label
              >Ministro</v-chip>
              <v-chip
                v-else
                color="success" size="x-small" label
              >Membro</v-chip>
            </div>
            <p class="text-body-2 text-medium-emphasis mt-1">@{{ authStore.user?.username }}</p>
            <p class="text-caption text-medium-emphasis">
              Membro desde {{ formatDate(authStore.user?.created_at) }}
            </p>
          </div>

          <v-btn
            variant="outlined"
            size="small"
            prepend-icon="mdi-pencil"
            class="text-none"
            @click="editDialog = true"
          >
            Editar perfil
          </v-btn>
        </div>
      </v-card-text>
    </v-card>

    <v-row>
      <!-- Coluna esquerda: info + paróquia -->
      <v-col cols="12" md="6">
        <!-- Informações pessoais -->
        <v-card class="mb-4" elevation="0" border>
          <v-card-title class="text-subtitle-1 font-weight-bold px-4 pt-4 pb-2">
            <v-icon start size="18">mdi-account-outline</v-icon>
            Informações
          </v-card-title>
          <v-divider />
          <v-list density="compact" lines="two">
            <v-list-item>
              <template #prepend><v-icon size="18" color="primary">mdi-email-outline</v-icon></template>
              <v-list-item-title class="text-caption text-medium-emphasis">Email</v-list-item-title>
              <v-list-item-subtitle class="text-body-2">{{ authStore.user?.email }}</v-list-item-subtitle>
            </v-list-item>
            <v-divider inset />
            <v-list-item>
              <template #prepend><v-icon size="18" color="primary">mdi-account-outline</v-icon></template>
              <v-list-item-title class="text-caption text-medium-emphasis">Nome completo</v-list-item-title>
              <v-list-item-subtitle class="text-body-2">{{ authStore.user?.full_name || '—' }}</v-list-item-subtitle>
            </v-list-item>
            <v-divider inset />
            <v-list-item>
              <template #prepend><v-icon size="18" color="primary">mdi-circle-outline</v-icon></template>
              <v-list-item-title class="text-caption text-medium-emphasis">Status</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip :color="authStore.user?.is_active ? 'success' : 'error'" size="x-small" label>
                  {{ authStore.user?.is_active ? 'Ativo' : 'Inativo' }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <!-- Coluna direita: paróquia -->
      <v-col cols="12" md="6">
        <v-card class="mb-4" elevation="0" border>
          <v-card-title class="text-subtitle-1 font-weight-bold px-4 pt-4 pb-2">
            <v-icon start size="18">mdi-church</v-icon>
            Paróquia
          </v-card-title>
          <v-divider />
          <v-card-text class="pa-4">
            <template v-if="authStore.parish?.name">
              <p class="text-body-1 font-weight-medium">{{ authStore.parish.name }}</p>
              <p v-if="authStore.parish?.diocese_name" class="text-caption text-medium-emphasis mt-1">
                {{ authStore.parish.diocese_name }}
              </p>
              <p v-if="authStore.parish?.address" class="text-caption text-medium-emphasis mt-1">
                <v-icon size="12" class="mr-1">mdi-map-marker-outline</v-icon>
                {{ authStore.parish.address }}
              </p>
            </template>
            <p v-else class="text-body-2 text-medium-emphasis">Nenhuma paróquia associada.</p>
          </v-card-text>
          <v-divider />
          <v-card-actions class="px-4 py-3">
            <v-btn
              variant="tonal"
              color="primary"
              size="small"
              prepend-icon="mdi-swap-horizontal"
              class="text-none"
              @click="parishDialog = true"
            >
              Trocar paróquia
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Ações da conta -->
    <v-card elevation="0" border>
      <v-card-text class="pa-4">
        <div class="d-flex justify-space-between align-center flex-wrap ga-2">
          <div>
            <p class="text-subtitle-2">Sair da conta</p>
            <p class="text-caption text-medium-emphasis">Encerra sua sessão neste dispositivo.</p>
          </div>
          <v-btn
            variant="outlined"
            color="error"
            size="small"
            prepend-icon="mdi-logout"
            class="text-none"
            @click="confirmLogout = true"
          >
            Sair
          </v-btn>
        </div>
      </v-card-text>
    </v-card>


    <!-- Dialog: Editar perfil -->
    <v-dialog v-model="editDialog" max-width="480" persistent>
      <v-card>
        <v-card-title class="text-h6 pa-5 pb-2">Editar perfil</v-card-title>
        <v-divider />
        <v-card-text class="pa-5">
          <v-form ref="editForm" v-model="editValid">
            <v-text-field
              v-model="editData.full_name"
              label="Nome completo"
              prepend-inner-icon="mdi-account"
              variant="outlined"
              density="comfortable"
              class="mb-3"
            />
            <v-text-field
              v-model="editData.username"
              label="Nome de usuário"
              prepend-inner-icon="mdi-at"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              :rules="[v => !!v || 'Obrigatório']"
            />
            <v-text-field
              v-model="editData.email"
              label="Email"
              prepend-inner-icon="mdi-email-outline"
              variant="outlined"
              density="comfortable"
              :rules="[v => !!v || 'Obrigatório', v => /.+@.+\..+/.test(v) || 'Email inválido']"
            />
          </v-form>
          <v-alert v-if="editError" type="error" density="compact" class="mt-2" variant="tonal">
            {{ editError }}
          </v-alert>
        </v-card-text>
        <v-divider />
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn variant="text" class="text-none" @click="editDialog = false">Cancelar</v-btn>
          <v-btn
            color="primary"
            variant="flat"
            class="text-none"
            :loading="editLoading"
            @click="saveProfile"
          >
            Salvar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


    <!-- Dialog: Trocar paróquia -->
    <v-dialog v-model="parishDialog" max-width="480" persistent>
      <v-card>
        <v-card-title class="text-h6 pa-5 pb-2">Trocar paróquia</v-card-title>
        <v-divider />
        <v-card-text class="pa-5">
          <p class="text-body-2 text-medium-emphasis mb-4">
            Selecione a paróquia que deseja se vincular. Isso irá atualizar sua sessão.
          </p>
          <v-autocomplete
            v-model="selectedParishSlug"
            :items="parishes"
            item-title="name"
            item-value="slug"
            label="Paróquia"
            prepend-inner-icon="mdi-church"
            variant="outlined"
            density="comfortable"
            :loading="loadingParishes"
            no-data-text="Nenhuma paróquia encontrada"
            clearable
          >
            <template #item="{ props, item }">
              <v-list-item v-bind="props" :subtitle="item.raw.diocese_name || item.raw.address || ''" />
            </template>
          </v-autocomplete>
          <v-alert v-if="parishError" type="error" density="compact" class="mt-2" variant="tonal">
            {{ parishError }}
          </v-alert>
        </v-card-text>
        <v-divider />
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn variant="text" class="text-none" @click="parishDialog = false">Cancelar</v-btn>
          <v-btn
            color="primary"
            variant="flat"
            class="text-none"
            :loading="parishLoading"
            :disabled="!selectedParishSlug"
            @click="doSwitchParish"
          >
            Confirmar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


    <!-- Dialog: Confirmar logout -->
    <v-dialog v-model="confirmLogout" max-width="360">
      <v-card>
        <v-card-title class="text-h6 pa-5 pb-2">Sair da conta</v-card-title>
        <v-card-text class="px-5 pb-2">Tem certeza que deseja encerrar sua sessão?</v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn variant="text" class="text-none" @click="confirmLogout = false">Cancelar</v-btn>
          <v-btn color="error" variant="flat" class="text-none" @click="logout">Sair</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script setup>
import { useAuthStore } from '~/stores/useAuthStore.js';

const authStore = useAuthStore();
const router = useRouter();

if (!authStore.user) router.push('/login');

// Computed
const initials = computed(() => {
  const name = authStore.user?.full_name || authStore.user?.username || '';
  return name.split(' ').slice(0, 2).map(n => n[0]?.toUpperCase()).join('');
});

const formatDate = (iso) => {
  if (!iso) return '—';
  return new Date(iso).toLocaleDateString('pt-BR');
};

// Edit profile
const editDialog = ref(false);
const editForm = ref(null);
const editValid = ref(false);
const editLoading = ref(false);
const editError = ref('');
const editData = reactive({
  full_name: authStore.user?.full_name || '',
  username:  authStore.user?.username || '',
  email:     authStore.user?.email || '',
});

watch(editDialog, (open) => {
  if (open) {
    editError.value = '';
    editData.full_name = authStore.user?.full_name || '';
    editData.username  = authStore.user?.username || '';
    editData.email     = authStore.user?.email || '';
  }
});

const saveProfile = async () => {
  const { valid } = await editForm.value.validate();
  if (!valid) return;
  editLoading.value = true;
  editError.value = '';
  try {
    await authStore.updateMe({ ...editData });
    editDialog.value = false;
  } catch (err) {
    editError.value = err?.data?.detail || 'Erro ao salvar perfil.';
  } finally {
    editLoading.value = false;
  }
};

// Switch parish
const parishDialog = ref(false);
const parishLoading = ref(false);
const parishError = ref('');
const selectedParishSlug = ref(null);
const parishes = ref([]);
const loadingParishes = ref(false);

watch(parishDialog, async (open) => {
  if (open) {
    parishError.value = '';
    selectedParishSlug.value = authStore.parish?.slug || null;
    if (!parishes.value.length) {
      loadingParishes.value = true;
      try {
        const { data } = await asyncUseApi('/parish/');
        parishes.value = data.value || [];
      } finally {
        loadingParishes.value = false;
      }
    }
  }
});

const doSwitchParish = async () => {
  if (!selectedParishSlug.value) return;
  parishLoading.value = true;
  parishError.value = '';
  try {
    await authStore.switchParish(selectedParishSlug.value);
    parishDialog.value = false;
  } catch (err) {
    parishError.value = err?.data?.detail || 'Erro ao trocar paróquia.';
  } finally {
    parishLoading.value = false;
  }
};

// Logout
const confirmLogout = ref(false);
const logout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.profile-header-card {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary), 0.04) 0%, transparent 60%);
}
</style>
