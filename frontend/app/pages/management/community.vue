<template>
  <v-container class="py-8" max-width="1000">

    <!-- Header -->
    <div class="d-flex align-center justify-space-between mb-6 flex-wrap ga-3">
      <div>
        <div class="d-flex align-center ga-2">
          <v-btn icon variant="text" size="small" to="/management">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
          <h1 class="text-h5 font-weight-bold">Comunidade</h1>
        </div>
        <p class="text-body-2 text-medium-emphasis mt-1 ml-10">
          Gerencie comunidades, grupos e pastorais da paróquia
        </p>
      </div>
      <v-btn
        color="primary"
        variant="flat"
        prepend-icon="mdi-plus"
        class="text-none"
        @click="openCreate()"
      >
        Novo
      </v-btn>
    </div>

    <!-- Tabs -->
    <v-tabs v-model="tab" color="primary" class="mb-4">
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

    <!-- Empty -->
    <div v-else-if="currentList.length === 0" class="d-flex flex-column align-center py-12 text-medium-emphasis">
      <v-icon size="52" class="mb-3 opacity-30">{{ TAB_META[tab].icon }}</v-icon>
      <p class="text-body-2">Nenhum{{ TAB_META[tab].feminin ? 'a' : '' }} {{ TAB_META[tab].label.toLowerCase() }} cadastrad{{ TAB_META[tab].feminin ? 'a' : 'o' }}. Use o botão "Novo" acima.</p>
    </div>

    <!-- Tabela -->
    <v-table v-else density="comfortable" class="rounded-lg border">
      <thead>
        <tr>
          <th>Nome</th>
          <th class="hidden-sm-and-down">{{ tab === 'comunidade' ? 'Responsável' : 'Coordenador' }}</th>
          <th v-if="tab !== 'comunidade'" class="hidden-sm-and-down">Reunião</th>
          <th v-if="tab === 'comunidade'" class="hidden-sm-and-down">Endereço</th>
          <th>Status</th>
          <th class="text-right">Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in currentList" :key="item.id">
          <td>
            <p class="text-body-2 font-weight-medium">{{ item.name }}</p>
            <p v-if="item.description" class="text-caption text-medium-emphasis">{{ item.description }}</p>
          </td>
          <td class="hidden-sm-and-down text-body-2">{{ item.coordinator || '—' }}</td>
          <td v-if="tab !== 'comunidade'" class="hidden-sm-and-down text-body-2">
            <span v-if="item.meeting_day">{{ formatDay(item.meeting_day) }}</span>
            <span v-if="item.meeting_time"> às {{ item.meeting_time }}</span>
            <span v-if="!item.meeting_day">—</span>
          </td>
          <td v-if="tab === 'comunidade'" class="hidden-sm-and-down text-body-2">{{ item.address || '—' }}</td>
          <td>
            <v-chip :color="item.is_active ? 'success' : 'default'" size="x-small" label>
              {{ item.is_active ? 'Ativo' : 'Inativo' }}
            </v-chip>
          </td>
          <td class="text-right">
            <v-btn icon size="small" variant="text" @click="openEdit(item)">
              <v-icon size="18">mdi-pencil-outline</v-icon>
            </v-btn>
            <v-btn icon size="small" variant="text" color="error" @click="confirmDelete(item)">
              <v-icon size="18">mdi-delete-outline</v-icon>
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>


    <!-- Dialog: Criar / Editar -->
    <v-dialog v-model="dialog" max-width="540" persistent>
      <v-card>
        <v-card-title class="text-h6 pa-5 pb-2">
          {{ editing ? 'Editar' : 'Nova' }} {{ FORM_LABELS[form.type] || 'Comunidade' }}
        </v-card-title>
        <v-divider />
        <v-card-text class="pa-5">
          <v-form ref="formRef" v-model="formValid">

            <!-- Tipo -->
            <v-btn-toggle v-model="form.type" mandatory density="compact" color="primary" class="mb-4 flex-wrap" rounded="lg">
              <v-btn value="comunidade" class="text-none" size="small">
                <v-icon start size="16">mdi-church</v-icon> Comunidade
              </v-btn>
              <v-btn value="grupo" class="text-none" size="small">
                <v-icon start size="16">mdi-account-group</v-icon> Grupo
              </v-btn>
              <v-btn value="pastoral" class="text-none" size="small">
                <v-icon start size="16">mdi-hands-pray</v-icon> Pastoral
              </v-btn>
            </v-btn-toggle>

            <v-text-field
              v-model="form.name"
              label="Nome *"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              :rules="[v => !!v || 'Obrigatório']"
            />
            <v-textarea
              v-model="form.description"
              label="Descrição"
              variant="outlined"
              density="comfortable"
              rows="2"
              class="mb-3"
            />
            <v-text-field
              v-model="form.coordinator"
              :label="form.type === 'comunidade' ? 'Responsável' : 'Coordenador(a)'"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              prepend-inner-icon="mdi-account-star-outline"
            />

            <v-text-field
              v-model="form.address"
              label="Endereço"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              prepend-inner-icon="mdi-map-marker-outline"
            />

            <!-- Reunião — só para grupos e pastorais -->
            <template v-if="form.type !== 'comunidade'">
              <v-row dense>
                <v-col cols="7">
                  <v-select
                    v-model="form.meeting_day"
                    :items="DAYS_OPTIONS"
                    label="Dia da reunião"
                    variant="outlined"
                    density="comfortable"
                    clearable
                  />
                </v-col>
                <v-col cols="5">
                  <v-text-field
                    v-model="form.meeting_time"
                    label="Horário"
                    variant="outlined"
                    density="comfortable"
                    placeholder="18:00"
                    prepend-inner-icon="mdi-clock-outline"
                  />
                </v-col>
              </v-row>
            </template>

            <v-switch
              v-if="editing"
              v-model="form.is_active"
              label="Ativo"
              color="primary"
              density="compact"
              hide-details
            />
          </v-form>
          <v-alert v-if="formError" type="error" density="compact" class="mt-2" variant="tonal">
            {{ formError }}
          </v-alert>
        </v-card-text>
        <v-divider />
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn variant="text" class="text-none" @click="dialog = false">Cancelar</v-btn>
          <v-btn
            color="primary"
            variant="flat"
            class="text-none"
            :loading="saving"
            @click="save"
          >
            {{ editing ? 'Salvar' : 'Criar' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


    <!-- Dialog: Confirmar desativação -->
    <v-dialog v-model="deleteDialog" max-width="380">
      <v-card>
        <v-card-title class="text-h6 pa-5 pb-2">Desativar</v-card-title>
        <v-card-text class="px-5 pb-2">
          Deseja desativar <strong>{{ deleteTarget?.name }}</strong>? Não aparecerá mais para os membros.
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn variant="text" class="text-none" @click="deleteDialog = false">Cancelar</v-btn>
          <v-btn color="error" variant="flat" class="text-none" :loading="deleting" @click="doDelete">
            Desativar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script setup>
import { useAuthStore } from '~/stores/useAuthStore.js';

const authStore = useAuthStore();
const tab = ref('comunidade');

const TAB_META = {
  comunidade: { label: 'Comunidade', icon: 'mdi-church',             feminin: true  },
  grupo:      { label: 'Grupo',      icon: 'mdi-account-group-outline', feminin: false },
  pastoral:   { label: 'Pastoral',   icon: 'mdi-hands-pray',          feminin: true  },
};

const FORM_LABELS = {
  comunidade: 'Comunidade',
  grupo:      'Grupo',
  pastoral:   'Pastoral',
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

const fetchAll = async () => {
  loading.value = true;
  try {
    const { data } = await asyncUseApi('/community/');
    allCommunities.value = data.value || [];
  } finally {
    loading.value = false;
  }
};
onMounted(fetchAll);

// Form
const dialog    = ref(false);
const formRef   = ref(null);
const formValid = ref(false);
const saving    = ref(false);
const formError = ref('');
const editing   = ref(null);

const emptyForm = () => ({
  type: tab.value,
  name: '',
  description: '',
  coordinator: '',
  meeting_day: null,
  meeting_time: '',
  address: '',
  is_active: true,
});
const form = reactive(emptyForm());

const openCreate = () => {
  Object.assign(form, emptyForm());
  editing.value = null;
  formError.value = '';
  dialog.value = true;
};

const openEdit = (item) => {
  Object.assign(form, { ...item });
  editing.value = item.id;
  formError.value = '';
  dialog.value = true;
};

const save = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;
  saving.value = true;
  formError.value = '';
  try {
    if (editing.value) {
      await asyncUseApi(`/community/${editing.value}`, { method: 'PATCH', body: { ...form } });
    } else {
      await asyncUseApi('/community/', { method: 'POST', body: { ...form } });
    }
    dialog.value = false;
    await fetchAll();
  } catch (err) {
    formError.value = err?.data?.detail || 'Erro ao salvar.';
  } finally {
    saving.value = false;
  }
};

// Delete
const deleteDialog = ref(false);
const deleteTarget = ref(null);
const deleting     = ref(false);

const confirmDelete = (item) => {
  deleteTarget.value = item;
  deleteDialog.value = true;
};

const doDelete = async () => {
  deleting.value = true;
  try {
    await asyncUseApi(`/community/${deleteTarget.value.id}`, { method: 'DELETE' });
    deleteDialog.value = false;
    await fetchAll();
  } finally {
    deleting.value = false;
  }
};

const DAYS_OPTIONS = [
  { title: 'Segunda-feira', value: 'segunda' },
  { title: 'Terça-feira',   value: 'terca'   },
  { title: 'Quarta-feira',  value: 'quarta'  },
  { title: 'Quinta-feira',  value: 'quinta'  },
  { title: 'Sexta-feira',   value: 'sexta'   },
  { title: 'Sábado',        value: 'sabado'  },
  { title: 'Domingo',       value: 'domingo' },
];
const DAYS_MAP = Object.fromEntries(DAYS_OPTIONS.map(d => [d.value, d.title]));
const formatDay = (d) => DAYS_MAP[d] || d;
</script>
