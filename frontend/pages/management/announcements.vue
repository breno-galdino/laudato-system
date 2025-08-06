
<template>
  <v-container>
    <v-row justify="space-between" align="center" class="mb-8">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Gerenciar Avisos</h1>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" @click="() => openModal()" prepend-icon="mdi-plus">
          Novo Aviso
        </v-btn>
      </v-col>
    </v-row>
    <v-list
      v-if="announcements.length > 0"
      class="pa-0"
      style="border: 1px solid rgb(var(--v-theme-primary)); border-radius: 12px; background: #fafbfc;"
      density="compact"
    >
      <v-list-item
        v-for="announcement in announcements"
        :key="announcement.id"
        class="d-flex align-center pa-2"
        style="border-bottom: 1.5px solid #e0e0e0;"
      >
        <div class="d-flex align-center" style="width: 100%;">
          <v-icon class="mr-3" size="32">{{ categories[announcement.category_id] }}</v-icon>
          <div class="flex-grow-1 d-flex flex-column">
            <div class="font-weight-bold text-body-1">{{ announcement.title }}</div>
            <div v-if="announcement.event_date" class="text-caption text-grey-darken-1">
              Data do Evento: {{ formatDate(announcement.event_date) }}
            </div>
            <div class="text-caption text-grey-darken-2">{{ announcement.content }}</div>
          </div>
          <div class="d-flex align-center" style="margin-left: auto;">
            <v-btn
              color="warning"
              variant="text"
              size="small"
              @click="openModal(announcement)"
              class="mr-2"
              style="min-width: 32px;"
            >
              Editar
            </v-btn>
            <v-btn
              color="error"
              variant="text"
              size="small"
              @click="deleteAnnouncement(announcement.id)"
              style="min-width: 32px;"
            >
              Excluir
            </v-btn>
          </div>
        </div>
      </v-list-item>
    </v-list>

    <div v-else class="text-center my-16">
      <v-icon size="64" color="grey-lighten-1">mdi-bell-off-outline</v-icon>
      <p class="text-h6 text-grey-darken-1 mt-4">Nenhum anúncio encontrado.</p>
      <p class="text-body-1 text-grey">Parece que ainda não há avisos disponíveis.</p>
    </div>

    <n-modal v-model:show="showModal" preset="dialog" :title="currentAnnouncement.id ? 'Editar Anúncio' : 'Novo Anúncio'"
      style="max-width: 600px">
      <n-form :model="currentAnnouncement" @submit.prevent="saveAnnouncement" label-placement="top">
        <n-form-item label="Título" path="title" required>
          <n-input v-model:value="currentAnnouncement.title" placeholder="Título" />
        </n-form-item>
        <n-form-item label="Descrição" path="content" required>
          <n-input v-model:value="currentAnnouncement.content" type="textarea" placeholder="Descrição" />
        </n-form-item>
        <n-form-item label="Categoria" path="category_id" required>
          <n-select v-model:value="currentAnnouncement.category_id" :options="categoryOptions"
            placeholder="Selecione uma categoria" />
        </n-form-item>
        <n-form-item label="Data do Evento" path="event_date" required>
          <n-date-picker v-model:value="currentAnnouncement.event_date" type="date" clearable style="width: 100%" />
        </n-form-item>
        <n-space justify="end">
          <n-button @click="closeModal" secondary> Cancelar </n-button>
          <n-button type="primary" attr-type="submit"> Salvar </n-button>
        </n-space>
      </n-form>
    </n-modal>
  </v-container>
</template>

<script setup>
const announcements = ref([]);
const categories = ref({});
const categoriesList = ref([]);
const showModal = ref(false);
const currentAnnouncement = ref({
  id: null,
  title: "",
  content: "",
  category_id: null,
  event_date: null,
});

const fetchAnnouncements = async () => {
  try {
    const { data } = await asyncUseApi("/warnings/");
    const { data: categoriesData } = await asyncUseApi("/category/");

    categoriesList.value = categoriesData.value;

    categoriesData.value.forEach((item) => {
      categories.value[item.id] = item.icon;
    });

    announcements.value = data.value;
  } catch (error) {
    console.error("Erro ao buscar anúncios:", error);
  }
};

const openModal = (announcement = null) => {
  if (announcement) {
    currentAnnouncement.value = { ...announcement };
  }
  showModal.value = true;
};

const closeModal = () => {
  currentAnnouncement.value = {
    id: null,
    title: "",
    description: "",
    category_id: null,
    event_date: null,
  };
  showModal.value = false;
};

const saveAnnouncement = async () => {
  currentAnnouncement.value.event_date = currentAnnouncement.value.event_date
    ? new Date(currentAnnouncement.value.event_date).toISOString()
    : null;
    
  try {
    if (currentAnnouncement.value.id) {
      await asyncUseApi(`/warnings/${currentAnnouncement.value.id}`, {
        method: "PUT",
        body: currentAnnouncement.value,
      });
    } else {
      await asyncUseApi("/warnings/", {
        method: "POST",
        body: currentAnnouncement.value,
      });
    }
    closeModal();
    fetchAnnouncements();
  } catch (error) {
    console.error("Erro ao salvar anúncio:", error);
  }
};

const deleteAnnouncement = async (id) => {
  try {
    await asyncUseApi(`/warnings/${id}`, {
      method: "DELETE",
    });
    fetchAnnouncements();
  } catch (error) {
    console.error("Erro ao excluir anúncio:", error);
  }
};

const formatDate = (dateStr) => {
  if (!dateStr || isNaN(new Date(dateStr).getTime())) return "";
  return new Date(dateStr).toLocaleDateString();
};

const categoryOptions = computed(() =>
  categoriesList.value.map((cat) => ({
    label: cat.name,
    value: cat.id,
  }))
);

onMounted(fetchAnnouncements);
</script>
