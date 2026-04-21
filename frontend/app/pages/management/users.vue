<template>
  <v-container class="py-8" max-width="900">

    <!-- Header -->
    <div class="d-flex align-center justify-space-between mb-6 flex-wrap ga-3">
      <div>
        <div class="d-flex align-center ga-2">
          <v-btn icon variant="text" size="small" to="/management">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
          <h1 class="text-h5 font-weight-bold">Usuários</h1>
        </div>
        <p class="text-body-2 text-medium-emphasis mt-1 ml-10">
          Membros e permissões — {{ authStore.parish?.name }}
        </p>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="d-flex justify-center py-12">
      <v-progress-circular indeterminate color="primary" />
    </div>

    <!-- Lista -->
    <template v-else>
      <!-- Barra de busca -->
      <v-text-field
        v-model="search"
        placeholder="Buscar por nome ou e-mail..."
        prepend-inner-icon="mdi-magnify"
        variant="outlined"
        density="comfortable"
        hide-details
        clearable
        class="mb-4"
      />

      <p class="text-caption text-medium-emphasis mb-3">
        {{ filteredUsers.length }} usuário{{ filteredUsers.length !== 1 ? 's' : '' }}
      </p>

      <v-card elevation="0" border rounded="lg">
        <v-list lines="two" class="pa-0">
          <template v-for="(user, i) in filteredUsers" :key="user.id">
            <v-divider v-if="i > 0" />
            <v-list-item class="px-4 py-3">
              <template #prepend>
                <v-avatar :color="roleColor(user.scopes)" size="40" class="mr-2">
                  <span class="text-caption font-weight-bold text-white">{{ initials(user) }}</span>
                </v-avatar>
              </template>

              <v-list-item-title class="text-body-2 font-weight-medium d-flex align-center ga-2 flex-wrap">
                {{ user.full_name || user.username }}
                <v-chip
                  v-for="s in displayScopes(user.scopes)"
                  :key="s.label"
                  :color="s.color"
                  size="x-small"
                  label
                >{{ s.label }}</v-chip>
                <v-chip v-if="!user.is_active" color="default" size="x-small" label>Inativo</v-chip>
                <v-chip v-if="user.id === authStore.user?.id" size="x-small" variant="outlined" label>você</v-chip>
              </v-list-item-title>
              <v-list-item-subtitle class="text-caption">
                @{{ user.username }} · {{ user.email }}
                · desde {{ formatDate(user.created_at) }}
              </v-list-item-subtitle>

              <template #append>
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  @click="openManage(user)"
                >
                  <v-icon size="18">mdi-shield-account-outline</v-icon>
                </v-btn>
              </template>
            </v-list-item>
          </template>

          <div v-if="filteredUsers.length === 0" class="text-center py-10 text-medium-emphasis text-body-2">
            Nenhum usuário encontrado.
          </div>
        </v-list>
      </v-card>
    </template>


    <!-- Dialog: Gerenciar permissões -->
    <v-dialog v-model="dialog" max-width="460">
      <v-card v-if="selected">
        <v-card-title class="text-h6 pa-5 pb-2 d-flex align-center ga-3">
          <v-avatar :color="roleColor(selected.scopes)" size="36">
            <span class="text-caption font-weight-bold text-white">{{ initials(selected) }}</span>
          </v-avatar>
          {{ selected.full_name || selected.username }}
        </v-card-title>
        <v-card-subtitle class="px-5 pb-3">@{{ selected.username }} · {{ selected.email }}</v-card-subtitle>
        <v-divider />

        <v-card-text class="pa-5">
          <p class="text-subtitle-2 font-weight-bold mb-3">Permissões</p>

          <div class="d-flex flex-column ga-3">
            <!-- Admin -->
            <v-card variant="outlined" rounded="lg" :color="selected.scopes.includes('admin') ? 'error' : ''">
              <v-card-text class="pa-3">
                <div class="d-flex align-center justify-space-between">
                  <div>
                    <p class="text-body-2 font-weight-medium d-flex align-center ga-1">
                      <v-icon size="16" color="error">mdi-shield-crown</v-icon>
                      Administrador
                    </p>
                    <p class="text-caption text-medium-emphasis">
                      Acesso total: gerenciar usuários, paróquia e todos os módulos.
                    </p>
                  </div>
                  <v-switch
                    :model-value="selected.scopes.includes('admin')"
                    :disabled="selected.id === authStore.user?.id"
                    color="error"
                    hide-details
                    density="compact"
                    @update:model-value="toggleScope(selected, 'admin', $event)"
                  />
                </div>
              </v-card-text>
            </v-card>

            <!-- Ministro -->
            <v-card variant="outlined" rounded="lg" :color="selected.scopes.includes('minister') ? 'warning' : ''">
              <v-card-text class="pa-3">
                <div class="d-flex align-center justify-space-between">
                  <div>
                    <p class="text-body-2 font-weight-medium d-flex align-center ga-1">
                      <v-icon size="16" color="warning">mdi-star-circle</v-icon>
                      Ministro
                    </p>
                    <p class="text-caption text-medium-emphasis">
                      Acesso à gestão (escalas, anúncios) sem controle de usuários.
                    </p>
                  </div>
                  <v-switch
                    :model-value="selected.scopes.includes('minister')"
                    color="warning"
                    hide-details
                    density="compact"
                    @update:model-value="toggleScope(selected, 'minister', $event)"
                  />
                </div>
              </v-card-text>
            </v-card>
          </div>

          <v-alert v-if="scopeError" type="error" density="compact" class="mt-3" variant="tonal">
            {{ scopeError }}
          </v-alert>
          <v-alert v-if="scopeSuccess" type="success" density="compact" class="mt-3" variant="tonal">
            {{ scopeSuccess }}
          </v-alert>
        </v-card-text>

        <v-divider />
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn variant="flat" color="primary" class="text-none" @click="dialog = false">Fechar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script setup>
import { useAuthStore } from '~/stores/useAuthStore.js';

const authStore = useAuthStore();

const users   = ref([]);
const loading = ref(true);
const search  = ref('');

const filteredUsers = computed(() => {
  const q = search.value?.toLowerCase() || '';
  if (!q) return users.value;
  return users.value.filter(u =>
    u.username?.toLowerCase().includes(q) ||
    u.full_name?.toLowerCase().includes(q) ||
    u.email?.toLowerCase().includes(q)
  );
});

const fetchUsers = async () => {
  loading.value = true;
  try {
    const { data } = await asyncUseApi('/auth/users/');
    users.value = data.value || [];
  } finally {
    loading.value = false;
  }
};
onMounted(fetchUsers);

// Helpers
const initials = (u) => (u.full_name || u.username || '?').split(' ').slice(0, 2).map(n => n[0]?.toUpperCase()).join('');
const formatDate = (iso) => iso ? new Date(iso).toLocaleDateString('pt-BR') : '—';

const SCOPE_DISPLAY = {
  admin:    { label: 'Admin',    color: 'error'   },
  minister: { label: 'Ministro', color: 'warning' },
};
const displayScopes = (scopes) =>
  (scopes || []).filter(s => SCOPE_DISPLAY[s]).map(s => SCOPE_DISPLAY[s]);

const roleColor = (scopes) => {
  if (scopes?.includes('admin'))    return 'error';
  if (scopes?.includes('minister')) return 'warning';
  return 'primary';
};

// Manage dialog
const dialog       = ref(false);
const selected     = ref(null);
const scopeError   = ref('');
const scopeSuccess = ref('');

const openManage = (user) => {
  selected.value   = { ...user, scopes: [...(user.scopes || [])] };
  scopeError.value   = '';
  scopeSuccess.value = '';
  dialog.value = true;
};

const toggleScope = async (user, scopeName, enable) => {
  scopeError.value   = '';
  scopeSuccess.value = '';
  try {
    if (enable) {
      await asyncUseApi(`/auth/users/${user.id}/scopes/${scopeName}`, { method: 'POST' });
      if (!selected.value.scopes.includes(scopeName)) selected.value.scopes.push(scopeName);
    } else {
      await asyncUseApi(`/auth/users/${user.id}/scopes/${scopeName}`, { method: 'DELETE' });
      selected.value.scopes = selected.value.scopes.filter(s => s !== scopeName);
    }
    // Atualiza lista local
    const u = users.value.find(u => u.id === user.id);
    if (u) u.scopes = [...selected.value.scopes];
    scopeSuccess.value = 'Permissão atualizada.';
    setTimeout(() => { scopeSuccess.value = ''; }, 2500);
  } catch (err) {
    scopeError.value = err?.data?.detail || 'Erro ao atualizar permissão.';
  }
};
</script>
