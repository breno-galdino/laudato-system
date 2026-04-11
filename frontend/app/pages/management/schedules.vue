<template>
  <v-container>
    <!-- Header -->
    <v-row justify="space-between" align="center" class="mb-8">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Escalas de Missas</h1>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" prepend-icon="mdi-plus" :loading="loadingCelebrations" @click="openCelebrationModal()">
          Nova Celebração
        </v-btn>
      </v-col>
    </v-row>

    <!-- Lista de Celebrações -->
    <v-expansion-panels v-if="celebrations.length > 0" variant="accordion">
      <v-expansion-panel v-for="celebration in celebrations" :key="celebration.id">
        <v-expansion-panel-title>
          <v-row align="center" no-gutters>
            <v-col>
              <span class="font-weight-bold">{{ formatDate(celebration.date) }}</span>
              <span v-if="celebration.description" class="text-grey-darken-1 ml-2">
                — {{ celebration.description }}
              </span>
            </v-col>
            <v-col cols="auto" class="mr-2">
              <v-chip size="small" color="primary" variant="tonal">
                {{ celebration.assignments.length }} escalado(s)
              </v-chip>
            </v-col>
          </v-row>
        </v-expansion-panel-title>

        <v-expansion-panel-text>
          <!-- Assignments da celebração -->
          <v-list v-if="celebration.assignments.length > 0" density="compact" class="mb-3">
            <v-list-item
              v-for="assignment in celebration.assignments"
              :key="assignment.id"
            >
              <template #prepend>
                <v-icon color="primary" class="mr-2">mdi-account</v-icon>
              </template>
              <v-list-item-title>
                {{ assignment.user_name }}
                <v-chip size="x-small" color="secondary" variant="tonal" class="ml-2">
                  {{ assignment.role_name }}
                </v-chip>
              </v-list-item-title>
              <template #append>
                <v-btn
                  icon size="small" variant="text" color="error"
                  :loading="deletingAssignmentId === assignment.id"
                  @click.stop="removeAssignment(celebration, assignment)"
                >
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </template>
            </v-list-item>
          </v-list>

          <p v-else class="text-grey text-body-2 mb-3">Nenhum escalado ainda.</p>

          <v-row>
            <v-col cols="auto">
              <v-btn
                color="primary" variant="tonal" size="small"
                prepend-icon="mdi-account-plus"
                @click="openAssignModal(celebration)"
              >
                Adicionar Escalado
              </v-btn>
            </v-col>
            <v-col cols="auto">
              <v-btn
                color="warning" variant="tonal" size="small"
                prepend-icon="mdi-pencil"
                @click="openCelebrationModal(celebration)"
              >
                Editar
              </v-btn>
            </v-col>
            <v-col cols="auto">
              <v-btn
                color="error" variant="tonal" size="small"
                prepend-icon="mdi-delete"
                :loading="deletingCelebrationId === celebration.id"
                @click="deleteCelebration(celebration)"
              >
                Excluir
              </v-btn>
            </v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <div v-else-if="!loadingCelebrations" class="text-center my-16">
      <v-icon size="64" color="grey-lighten-1">mdi-calendar-blank-outline</v-icon>
      <p class="text-h6 text-grey-darken-1 mt-4">Nenhuma celebração cadastrada.</p>
      <p class="text-body-1 text-grey">Crie a primeira celebração clicando em "Nova Celebração".</p>
    </div>

    <!-- Modal: Criar / Editar Celebração -->
    <n-modal
      v-model:show="showCelebrationModal"
      preset="dialog"
      :title="currentCelebration.id ? 'Editar Celebração' : 'Nova Celebração'"
      style="max-width: 500px"
    >
      <n-form :model="currentCelebration" label-placement="top">
        <n-form-item label="Data e Hora" required>
          <n-date-picker
            v-model:value="currentCelebration.date"
            type="datetime"
            clearable
            style="width: 100%"
            format="dd/MM/yyyy HH:mm"
          />
        </n-form-item>
        <n-form-item label="Descrição">
          <n-input
            v-model:value="currentCelebration.description"
            placeholder="Ex: Missa das 10h, Missa de domingo..."
          />
        </n-form-item>
      </n-form>
      <template #action>
        <n-button @click="showCelebrationModal = false">Cancelar</n-button>
        <n-button type="primary" :loading="savingCelebration" @click="saveCelebration">
          Salvar
        </n-button>
      </template>
    </n-modal>

    <!-- Modal: Adicionar Escalado -->
    <n-modal
      v-model:show="showAssignModal"
      preset="dialog"
      title="Adicionar Escalado"
      style="max-width: 460px"
    >
      <n-form :model="assignForm" label-placement="top">
        <n-form-item label="Usuário" required>
          <n-select
            v-model:value="assignForm.user_id"
            :options="userOptions"
            placeholder="Selecione o usuário"
            filterable
          />
        </n-form-item>
        <n-form-item label="Função" required>
          <n-select
            v-model:value="assignForm.role_id"
            :options="roleOptions"
            placeholder="Selecione a função"
          />
        </n-form-item>
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
const celebrations = ref([])
const roles = ref([])
const users = ref([])

const loadingCelebrations = ref(false)
const savingCelebration = ref(false)
const deletingCelebrationId = ref(null)
const deletingAssignmentId = ref(null)
const savingAssignment = ref(false)

const showCelebrationModal = ref(false)
const showAssignModal = ref(false)

const currentCelebration = ref({ id: null, date: null, description: '' })
const currentCelebrationForAssign = ref(null)
const assignForm = ref({ user_id: null, role_id: null })

// --- Fetch ---

const fetchAll = async () => {
  loadingCelebrations.value = true
  try {
    const [{ data: celebData }, { data: rolesData }, { data: usersData }] = await Promise.all([
      asyncUseApi('/celebration/'),
      asyncUseApi('/celebration/roles/'),
      asyncUseApi('/auth/users/'),
    ])
    celebrations.value = celebData.value ?? []
    roles.value = rolesData.value ?? []
    users.value = usersData.value ?? []
  } catch (e) {
    console.error('Erro ao carregar dados:', e)
  } finally {
    loadingCelebrations.value = false
  }
}

// --- Options para selects ---

const roleOptions = computed(() =>
  roles.value.map(r => ({ label: r.name, value: r.id }))
)

const userOptions = computed(() =>
  users.value.map(u => ({ label: u.username, value: u.id }))
)

// --- Celebração CRUD ---

const openCelebrationModal = (celebration = null) => {
  if (celebration) {
    currentCelebration.value = {
      id: celebration.id,
      date: new Date(celebration.date).getTime(),
      description: celebration.description ?? '',
    }
  } else {
    currentCelebration.value = { id: null, date: null, description: '' }
  }
  showCelebrationModal.value = true
}

const saveCelebration = async () => {
  if (!currentCelebration.value.date) return
  savingCelebration.value = true
  try {
    const body = {
      date: new Date(currentCelebration.value.date).toISOString(),
      description: currentCelebration.value.description || null,
    }
    if (currentCelebration.value.id) {
      await asyncUseApi(`/celebration/${currentCelebration.value.id}`, { method: 'PUT', body })
      message.success('Celebração atualizada.')
    } else {
      await asyncUseApi('/celebration/', { method: 'POST', body })
      message.success('Celebração criada.')
    }
    showCelebrationModal.value = false
    await fetchAll()
  } catch (e) {
    message.error('Erro ao salvar celebração.')
    console.error(e)
  } finally {
    savingCelebration.value = false
  }
}

const deleteCelebration = (celebration) => {
  dialog.warning({
    title: 'Excluir celebração',
    content: `Deseja excluir "${formatDate(celebration.date)}"? Todos os escalados serão removidos.`,
    positiveText: 'Sim, excluir',
    negativeText: 'Cancelar',
    draggable: true,
    onPositiveClick: async () => {
      deletingCelebrationId.value = celebration.id
      try {
        await asyncUseApi(`/celebration/${celebration.id}`, { method: 'DELETE' })
        message.success('Celebração excluída.')
        await fetchAll()
      } catch (e) {
        message.error('Erro ao excluir celebração.')
      } finally {
        deletingCelebrationId.value = null
      }
    },
    onNegativeClick: () => message.info('Ação cancelada.'),
  })
}

// --- Assignment ---

const openAssignModal = (celebration) => {
  currentCelebrationForAssign.value = celebration
  assignForm.value = { user_id: null, role_id: null }
  showAssignModal.value = true
}

const saveAssignment = async () => {
  if (!assignForm.value.user_id || !assignForm.value.role_id) return
  savingAssignment.value = true
  try {
    await asyncUseApi(`/celebration/assign?celebration_id=${currentCelebrationForAssign.value.id}`, {
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

const removeAssignment = (celebration, assignment) => {
  dialog.warning({
    title: 'Remover escalado',
    content: `Remover ${assignment.user_name} (${assignment.role_name}) desta celebração?`,
    positiveText: 'Sim',
    negativeText: 'Cancelar',
    draggable: true,
    onPositiveClick: async () => {
      deletingAssignmentId.value = assignment.id
      try {
        await asyncUseApi(`/celebration/assign/${assignment.id}`, { method: 'DELETE' })
        message.success('Escalado removido.')
        await fetchAll()
      } catch (e) {
        message.error('Erro ao remover escalado.')
      } finally {
        deletingAssignmentId.value = null
      }
    },
    onNegativeClick: () => message.info('Ação cancelada.'),
  })
}

// --- Helpers ---

const formatDate = (d) => {
  if (!d) return ''
  return new Date(d).toLocaleString('pt-BR', {
    weekday: 'long',
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(fetchAll)
</script>
