<template>
  <v-container>
    <v-row justify="space-between" align="center" class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Avisos</h1>
        <p class="text-body-2 text-grey-darken-1 mt-1">Gerencie os avisos e eventos da paróquia</p>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" prepend-icon="mdi-plus" :loading="loading" rounded="pill" @click="openModal()">
          Novo Aviso
        </v-btn>
      </v-col>
    </v-row>

    <div v-if="loading" class="d-flex justify-center py-16">
      <v-progress-circular indeterminate color="primary" size="48" />
    </div>

    <v-row v-else-if="announcements.length > 0">
      <v-col v-for="a in announcements" :key="a.id" cols="12" md="6">
        <v-card rounded="lg" variant="outlined" class="announcement-card h-100">
          <v-card-item class="pb-2">
            <template #prepend>
              <v-avatar :color="categoryColor(a.category_id)" variant="tonal" size="40">
                <v-icon size="20">{{ categories[a.category_id] ?? 'mdi-bell-outline' }}</v-icon>
              </v-avatar>
            </template>
            <v-card-title class="text-body-1 font-weight-bold">{{ a.title }}</v-card-title>
            <v-card-subtitle class="text-caption">{{ categoriesName[a.category_id] }}</v-card-subtitle>
            <template #append>
              <v-menu>
                <template #activator="{ props }">
                  <v-btn v-bind="props" icon="mdi-dots-vertical" variant="text" size="small" />
                </template>
                <v-list density="compact" min-width="140">
                  <v-list-item prepend-icon="mdi-pencil-outline" title="Editar" @click="openModal(a)" />
                  <v-list-item prepend-icon="mdi-delete-outline" title="Excluir" class="text-error" @click="confirmDelete(a)" />
                </v-list>
              </v-menu>
            </template>
          </v-card-item>

          <v-card-text class="pt-1">
            <p class="text-body-2 text-grey-darken-2 mb-3">{{ a.content }}</p>
            <div class="d-flex flex-wrap ga-2">
              <v-chip
                v-if="a.community_id"
                size="x-small"
                color="secondary"
                variant="tonal"
                prepend-icon="mdi-map-marker-outline"
              >
                {{ communityMap[a.community_id] ?? 'Comunidade' }}
              </v-chip>
              <v-chip v-else size="x-small" color="grey" variant="tonal" prepend-icon="mdi-earth">
                Todas as comunidades
              </v-chip>
              <v-chip v-if="a.event_date" size="x-small" color="primary" variant="tonal" prepend-icon="mdi-calendar-outline">
                {{ formatDate(a.event_date) }}
              </v-chip>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <div v-else class="text-center py-20">
      <v-icon size="72" color="grey-lighten-2">mdi-bell-off-outline</v-icon>
      <p class="text-h6 text-grey-darken-1 mt-4">Nenhum aviso encontrado</p>
      <p class="text-body-2 text-grey">Crie o primeiro aviso clicando em "Novo Aviso".</p>
    </div>

    <!-- Modal -->
    <n-modal
      v-model:show="showModal"
      preset="dialog"
      :title="form.id ? 'Editar Aviso' : 'Novo Aviso'"
      style="max-width: 580px"
    >
      <n-form :model="form" @submit.prevent="save" label-placement="top">
        <n-form-item label="Título" required>
          <n-input v-model:value="form.title" placeholder="Ex: Missa de Natal" />
        </n-form-item>
        <n-form-item label="Descrição" required>
          <n-input v-model:value="form.content" type="textarea" :rows="3" placeholder="Detalhes do aviso..." />
        </n-form-item>
        <n-grid :cols="2" :x-gap="12">
          <n-form-item-gi label="Categoria" required>
            <n-select v-model:value="form.category_id" :options="categoryOptions" placeholder="Selecione" />
          </n-form-item-gi>
          <n-form-item-gi label="Local (opcional)">
            <n-select
              v-model:value="form.community_id"
              :options="communityOptions"
              placeholder="Todas as comunidades"
              clearable
            />
          </n-form-item-gi>
        </n-grid>
        <n-form-item label="Data do Evento (opcional)">
          <n-date-picker
            v-model:value="form.event_date"
            type="date"
            clearable
            style="width: 100%"
            format="dd/MM/yyyy"
          />
        </n-form-item>
        <n-space justify="end">
          <n-button @click="showModal = false" secondary>Cancelar</n-button>
          <n-button type="primary" attr-type="submit" :loading="saving">Salvar</n-button>
        </n-space>
      </n-form>
    </n-modal>
  </v-container>
</template>

<script setup>
const config = useRuntimeConfig()
const { useAuthStore } = await import('~/stores/useAuthStore.js')
const authStore = useAuthStore()

const announcements = ref([])
const categories = ref({})
const categoriesName = ref({})
const categoriesList = ref([])
const communities = ref([])
const loading = ref(false)
const saving = ref(false)
const showModal = ref(false)

const emptyForm = () => ({ id: null, title: '', content: '', category_id: null, community_id: null, event_date: null })
const form = ref(emptyForm())

const apiBase = config.public.apiUrl.replace(/\/$/, '')
const slug = authStore.parishSlug

const apiFetch = (path, opts = {}) =>
  $fetch(`${apiBase}${path}`, { credentials: 'include', ...opts })

const publicFetch = (path) =>
  $fetch(`${apiBase}${path}${path.includes('?') ? '&' : '?'}parish_slug=${slug}`, { credentials: 'include' })

const fetchAll = async () => {
  loading.value = true
  try {
    const [warns, cats, comms] = await Promise.all([
      publicFetch('/warnings/'),
      publicFetch('/category/'),
      apiFetch('/community/?type=comunidade'),
    ])

    categoriesList.value = cats
    cats.forEach(c => {
      categories.value[c.id] = c.icon
      categoriesName.value[c.id] = c.name
    })
    communities.value = comms
    announcements.value = warns
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const communityMap = computed(() =>
  Object.fromEntries(communities.value.map(c => [c.id, c.name]))
)

const categoryOptions = computed(() =>
  categoriesList.value.map(c => ({ label: c.name, value: c.id }))
)

const communityOptions = computed(() =>
  communities.value.map(c => ({ label: c.name, value: c.id }))
)

const categoryColor = (id) => {
  const colors = ['primary', 'secondary', 'success', 'warning', 'info', 'error']
  return colors[id % colors.length] ?? 'primary'
}

const openModal = (a = null) => {
  form.value = a
    ? { ...a, event_date: a.event_date ? new Date(a.event_date).getTime() : null }
    : emptyForm()
  showModal.value = true
}

const save = async () => {
  saving.value = true
  try {
    const body = {
      ...form.value,
      event_date: form.value.event_date
        ? new Date(form.value.event_date).toISOString()
        : null,
    }
    if (body.id) {
      await apiFetch(`/warnings/${body.id}`, { method: 'PUT', body })
    } else {
      await apiFetch('/warnings/', { method: 'POST', body })
    }
    showModal.value = false
    message.success(body.id ? 'Aviso atualizado.' : 'Aviso criado.')
    await fetchAll()
  } catch (e) {
    message.error('Erro ao salvar aviso.')
    console.error(e)
  } finally {
    saving.value = false
  }
}

const confirmDelete = (a) => {
  dialog.warning({
    title: 'Excluir aviso',
    content: `Deseja excluir "${a.title}"?`,
    positiveText: 'Sim, excluir',
    negativeText: 'Cancelar',
    draggable: true,
    onPositiveClick: async () => {
      try {
        await apiFetch(`/warnings/${a.id}`, { method: 'DELETE' })
        message.success('Aviso excluído.')
        await fetchAll()
      } catch (e) {
        message.error('Erro ao excluir aviso.')
      }
    },
    onNegativeClick: () => message.info('Ação cancelada.'),
  })
}

const formatDate = (d) => {
  if (!d || isNaN(new Date(d).getTime())) return ''
  return new Date(d).toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })
}

onMounted(fetchAll)
</script>

<style scoped>
.announcement-card {
  transition: box-shadow 0.2s;
}
.announcement-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
}
</style>
