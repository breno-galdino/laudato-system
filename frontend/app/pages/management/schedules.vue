<template>
  <v-container>
    <v-row justify="space-between" align="center" class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Escalas de Missas</h1>
        <p class="text-body-2 text-grey-darken-1 mt-1">Gerencie celebrações e escalados da paróquia</p>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" prepend-icon="mdi-plus" rounded="pill" :loading="loading" @click="openCelebrationModal()">
          Nova Missa
        </v-btn>
      </v-col>
    </v-row>

    <div v-if="loading" class="d-flex justify-center py-16">
      <v-progress-circular indeterminate color="primary" size="48" />
    </div>

    <v-row v-else-if="celebrations.length">
      <v-col v-for="cel in celebrations" :key="cel.id" cols="12" md="6">
        <v-card rounded="lg" variant="outlined" class="celebration-card h-100">
          <v-card-item class="pb-2">
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
            <v-card-subtitle class="d-flex flex-wrap align-center ga-1 mt-1">
              <span class="text-caption">{{ celWeekday(cel.date) }}</span>
              <v-chip size="x-small" color="primary" variant="tonal">
                {{ cel.assignments.length }} escalado(s)
              </v-chip>
              <v-chip v-if="cel.community_id" size="x-small" color="secondary" variant="tonal" prepend-icon="mdi-map-marker-outline">
                {{ communityMap[cel.community_id] ?? 'Comunidade' }}
              </v-chip>
            </v-card-subtitle>
            <template #append>
              <v-menu>
                <template #activator="{ props }">
                  <v-btn v-bind="props" icon="mdi-dots-vertical" variant="text" size="small" />
                </template>
                <v-list density="compact" min-width="160">
                  <v-list-item prepend-icon="mdi-account-plus-outline" title="Adicionar escalado" @click="openAssignModal(cel)" />
                  <v-list-item prepend-icon="mdi-pencil-outline" title="Editar" @click="openCelebrationModal(cel)" />
                  <v-list-item prepend-icon="mdi-delete-outline" title="Excluir" class="text-error" @click="confirmDelete(cel)" />
                </v-list>
              </v-menu>
            </template>
          </v-card-item>

          <v-card-text class="pt-1">
            <div v-if="cel.assignments.length" class="d-flex flex-wrap ga-2">
              <v-chip
                v-for="a in cel.assignments"
                :key="a.id"
                size="small"
                variant="tonal"
                color="secondary"
                closable
                :disabled="removingId === a.id"
                @click:close="confirmRemoveAssignment(cel, a)"
              >
                <v-icon start size="14">mdi-account</v-icon>
                {{ a.user_name }}
                <span class="text-caption opacity-70 ml-1">· {{ a.role_name }}</span>
              </v-chip>
            </div>
            <p v-else class="text-body-2 text-grey">Nenhum escalado ainda.</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <div v-else class="text-center py-20">
      <v-icon size="72" color="grey-lighten-2">mdi-calendar-blank-outline</v-icon>
      <p class="text-h6 text-grey-darken-1 mt-4">Nenhuma Missa cadastrada</p>
      <p class="text-body-2 text-grey">Crie a primeira Missa clicando em "Nova Missa".</p>
    </div>

    <!-- Modal: Criar / Editar Missa -->
    <n-modal
      v-model:show="showCelebrationModal"
      preset="dialog"
      :title="celebForm.id ? 'Editar Missa' : 'Nova Missa'"
      style="max-width: 480px"
    >
      <n-form :model="celebForm" label-placement="top">
        <n-form-item label="Data e Hora" required>
          <n-date-picker
            v-model:value="celebForm.date"
            type="datetime"
            clearable
            style="width: 100%"
            format="dd/MM/yyyy HH:mm"
          />
        </n-form-item>
        <n-form-item label="Descrição (opcional)">
          <n-input v-model:value="celebForm.description" placeholder="Ex: Missa das 10h, Missa de domingo..." />
        </n-form-item>
        <n-form-item label="Local (opcional)">
          <n-select
            v-model:value="celebForm.community_id"
            :options="communityOptions"
            placeholder="Todas as comunidades"
            clearable
          />
        </n-form-item>
      </n-form>
      <template #action>
        <n-button @click="showCelebrationModal = false">Cancelar</n-button>
        <n-button type="primary" :loading="savingCelebration" @click="saveCelebration">Salvar</n-button>
      </template>
    </n-modal>

    <!-- Modal: Adicionar Escalado -->
    <n-modal
      v-model:show="showAssignModal"
      preset="dialog"
      title="Adicionar Escalado"
      style="max-width: 440px"
    >
      <n-form :model="assignForm" label-placement="top">
        <n-grid :cols="1" :y-gap="4">
          <n-form-item-gi label="Usuário" required>
            <n-select
              v-model:value="assignForm.user_id"
              :options="userOptions"
              placeholder="Selecione o usuário"
              filterable
            />
          </n-form-item-gi>
          <n-form-item-gi label="Função" required>
            <n-select
              v-model:value="assignForm.role_id"
              :options="roleOptions"
              placeholder="Selecione a função"
            />
          </n-form-item-gi>
        </n-grid>
      </n-form>
      <template #action>
        <n-button @click="showAssignModal = false">Cancelar</n-button>
        <n-button
          type="primary"
          :loading="savingAssignment"
          :disabled="!assignForm.user_id || !assignForm.role_id"
          @click="saveAssignment"
        >
          Adicionar
        </n-button>
      </template>
    </n-modal>
  </v-container>
</template>

<script setup>
const config = useRuntimeConfig()
const apiBase = config.public.apiUrl.replace(/\/$/, '')

const apiFetch = (path, opts = {}) =>
  $fetch(`${apiBase}${path}`, { credentials: 'include', ...opts })

const celebrations = ref([])
const roles = ref([])
const users = ref([])
const communities = ref([])
const loading = ref(false)
const savingCelebration = ref(false)
const savingAssignment = ref(false)
const removingId = ref(null)

const showCelebrationModal = ref(false)
const showAssignModal = ref(false)

const emptyCelebForm = () => ({ id: null, date: null, description: '', community_id: null })
const celebForm = ref(emptyCelebForm())
const assignForm = ref({ user_id: null, role_id: null })
const currentCelebrationForAssign = ref(null)

const fetchAll = async () => {
  loading.value = true
  try {
    const [cels, r, u, comms] = await Promise.all([
      apiFetch('/celebration/'),
      apiFetch('/celebration/roles/'),
      apiFetch('/auth/users/'),
      apiFetch('/community/?type=comunidade'),
    ])
    celebrations.value = cels
    roles.value = r
    users.value = u
    communities.value = comms
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const roleOptions = computed(() => roles.value.map(r => ({ label: r.name, value: r.id })))
const userOptions = computed(() => users.value.map(u => ({ label: u.username, value: u.id })))
const communityOptions = computed(() => communities.value.map(c => ({ label: c.name, value: c.id })))
const communityMap = computed(() => Object.fromEntries(communities.value.map(c => [c.id, c.name])))

// ── Missa ──────────────────────────────────

const openCelebrationModal = (cel = null) => {
  celebForm.value = cel
    ? { id: cel.id, date: new Date(cel.date).getTime(), description: cel.description ?? '', community_id: cel.community_id ?? null }
    : emptyCelebForm()
  showCelebrationModal.value = true
}

const saveCelebration = async () => {
  if (!celebForm.value.date) return
  savingCelebration.value = true
  try {
    const body = {
      date: new Date(celebForm.value.date).toISOString(),
      description: celebForm.value.description || null,
      community_id: celebForm.value.community_id ?? null,
    }
    if (celebForm.value.id) {
      await apiFetch(`/celebration/${celebForm.value.id}`, { method: 'PUT', body })
      message.success('Missa atualizada.')
    } else {
      await apiFetch('/celebration/', { method: 'POST', body })
      message.success('Missa criada.')
    }
    showCelebrationModal.value = false
    await fetchAll()
  } catch (e) {
    message.error('Erro ao salvar Missa.')
    console.error(e)
  } finally {
    savingCelebration.value = false
  }
}

const confirmDelete = (cel) => {
  dialog.warning({
    title: 'Excluir Missa',
    content: `Deseja excluir a Missa de ${celDay(cel.date)}/${celMonth(cel.date)}? Todos os escalados serão removidos.`,
    positiveText: 'Sim, excluir',
    negativeText: 'Cancelar',
    draggable: true,
    onPositiveClick: async () => {
      try {
        await apiFetch(`/celebration/${cel.id}`, { method: 'DELETE' })
        message.success('Missa excluída.')
        await fetchAll()
      } catch (e) {
        message.error('Erro ao excluir Missa.')
      }
    },
    onNegativeClick: () => message.info('Ação cancelada.'),
  })
}

// ── Escalados ───────────────────────────────────

const openAssignModal = (cel) => {
  currentCelebrationForAssign.value = cel
  assignForm.value = { user_id: null, role_id: null }
  showAssignModal.value = true
}

const saveAssignment = async () => {
  if (!assignForm.value.user_id || !assignForm.value.role_id) return
  savingAssignment.value = true
  try {
    await apiFetch(`/celebration/assign?celebration_id=${currentCelebrationForAssign.value.id}`, {
      method: 'POST',
      body: [{ user_id: assignForm.value.user_id, role_id: assignForm.value.role_id }],
    })
    message.success('Escalado adicionado.')
    showAssignModal.value = false
    await fetchAll()
  } catch (e) {
    message.error('Erro ao adicionar escalado.')
    console.error(e)
  } finally {
    savingAssignment.value = false
  }
}

const confirmRemoveAssignment = (cel, assignment) => {
  dialog.warning({
    title: 'Remover escalado',
    content: `Remover ${assignment.user_name} (${assignment.role_name})?`,
    positiveText: 'Sim',
    negativeText: 'Cancelar',
    draggable: true,
    onPositiveClick: async () => {
      removingId.value = assignment.id
      try {
        await apiFetch(`/celebration/assign/${assignment.id}`, { method: 'DELETE' })
        message.success('Escalado removido.')
        await fetchAll()
      } catch (e) {
        message.error('Erro ao remover escalado.')
      } finally {
        removingId.value = null
      }
    },
    onNegativeClick: () => message.info('Ação cancelada.'),
  })
}

// ── Formatação ──────────────────────────────────

const celDay     = (d) => new Date(d).getDate().toString().padStart(2, '0')
const celMonth   = (d) => new Date(d).toLocaleDateString('pt-BR', { month: 'short' }).replace('.', '')
const celTime    = (d) => new Date(d).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
const celWeekday = (d) => new Date(d).toLocaleDateString('pt-BR', { weekday: 'long', day: '2-digit', month: 'long', year: 'numeric' })

onMounted(fetchAll)
</script>

<style scoped>
.celebration-card {
  transition: box-shadow 0.2s;
}
.celebration-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
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
</style>
