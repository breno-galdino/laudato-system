<template>
  <n-space vertical size="large" class="py-8">
    <n-space justify="space-between" align="center" class="mb-8">
      <h1 class="text-4xl font-bold text-gray-800">Gerenciar Anúncios</h1>
      <n-button type="primary" @click="()=>openModal()" icon="plus">
        Novo Anúncio
      </n-button>
    </n-space>

    <n-grid v-if="announcements.length > 0" :cols="12" :x-gap="16" :y-gap="16">
      <n-grid-item
        v-for="announcement in announcements"
        :key="announcement.id"
        :span="12"
        :md="6"
        :lg="4"
      >
        <n-card class="hover:scale-105 transition-transform duration-300">
          <template #header>
            <span class="text-h6">{{ announcement.title }}</span>
          </template>
          <template #header-extra>
            <span v-if="announcement.event_date" class="text-xs text-gray-500">
              Data do Evento: {{ formatDate(announcement.event_date) }}
            </span>
          </template>
          <div>{{ announcement.content }}</div>
          <template #footer>
            <n-space>
              <n-button type="warning" @click="openModal(announcement)" secondary>
                Editar
              </n-button>
              <n-button type="error" @click="deleteAnnouncement(announcement.id)" secondary>
                Excluir
              </n-button>
            </n-space>
          </template>
        </n-card>
      </n-grid-item>
    </n-grid>

    <div v-else class="text-center">
      <n-empty description="Parece que ainda não há anúncios disponíveis.">
        <template #extra>
          <p>Nenhum anúncio encontrado.</p>
        </template>
      </n-empty>
    </div>

    <n-modal v-model:show="showModal" preset="dialog" style="max-width:600px;">
      <template #header>
        <span class="text-h5">{{ currentAnnouncement.id ? 'Editar Anúncio' : 'Novo Anúncio' }}</span>
      </template>
      <n-form
        :model="currentAnnouncement"
        @submit.prevent="saveAnnouncement"
        label-placement="top"
      >
        <n-form-item label="Título" path="title" required>
          <n-input v-model:value="currentAnnouncement.title" placeholder="Título" />
        </n-form-item>
        <n-form-item label="Descrição" path="content" required>
          <n-input
            v-model:value="currentAnnouncement.content"
            type="textarea"
            placeholder="Descrição"
          />
        </n-form-item>
        <n-form-item label="Categoria" path="category_id" required>
          <n-select
            v-model:value="currentAnnouncement.category_id"
            :options="categoryOptions"
            placeholder="Selecione uma categoria"
          />
        </n-form-item>
        <n-form-item label="Data do Evento" path="event_date" required>
          <n-date-picker
            v-model:value="currentAnnouncement.event_date"
            type="date"
            clearable
            style="width: 100%;"
          />
        </n-form-item>
        <n-space justify="end">
          <n-button @click="closeModal" secondary>
            Cancelar
          </n-button>
          <n-button type="primary" attr-type="submit">
            Salvar
          </n-button>
        </n-space>
      </n-form>
    </n-modal>
  </n-space>
</template>

<script setup>
const announcements = ref([])
const categories = ref([])
const showModal = ref(false)
const currentAnnouncement = ref({
  id: null,
  title: '',
  content: '',
  category_id: null,
  event_date: null,
})

const fetchAnnouncements = async () => {
  try {
    const { data } = await asyncUseApi('/warnings')
    const { data: categoriesData } = await asyncUseApi('/category')
    categories.value = categoriesData.value
    announcements.value = data.value
  } catch (error) {
    console.error('Erro ao buscar anúncios:', error)
  }
}

const openModal = (announcement = null) => {
  if (announcement) {
    currentAnnouncement.value = { ...announcement }
  }
  showModal.value = true
}

const closeModal = () => {
  currentAnnouncement.value = {
    id: null,
    title: '',
    description: '',
    category_id: null,
    event_date: null,
  }
  showModal.value = false
}

const saveAnnouncement = async () => {
  currentAnnouncement.value.event_date = currentAnnouncement.value.event_date
  ? new Date(currentAnnouncement.value.event_date).toISOString()
  : null
  console.log('Salvando anúncio:', currentAnnouncement.value)
  try {
    if (currentAnnouncement.value.id) {
      await asyncUseApi(`/warnings/${currentAnnouncement.value.id}`, {
        method: 'PUT',
        body: currentAnnouncement.value,
      })
    } else {
      useApi('/warnings', {
        method: 'POST',
        body: currentAnnouncement.value,
      })
    }
    closeModal()
    fetchAnnouncements()
  } catch (error) {
    console.error('Erro ao salvar anúncio:', error)
  }
}

const deleteAnnouncement = async (id) => {
  try {
    await asyncUseApi(`/warnings/${id}`, {
      method: 'DELETE',
    })
    fetchAnnouncements()
  } catch (error) {
    console.error('Erro ao excluir anúncio:', error)
  }
}

const formatDate = (dateStr) => {
  if (!dateStr || isNaN(new Date(dateStr).getTime())) return ''
  return new Date(dateStr).toLocaleDateString()
}

const categoryOptions = computed(() =>
  categories.value.map((cat) => ({
    label: cat.name,
    value: cat.id,
  }))
)

onMounted(fetchAnnouncements)
</script>