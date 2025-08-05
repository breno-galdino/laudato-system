
<template>
  <v-container>
    <v-row justify="space-between" align="center" class="mb-8">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Gerenciar Anúncios</h1>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" @click="() => openModal()" prepend-icon="mdi-plus">
          Novo Anúncio
        </v-btn>
      </v-col>
    </v-row>

    <v-row v-if="announcements.length > 0">
      <v-col v-for="announcement in announcements" :key="announcement.id" cols="12" md="6" lg="4">
        <v-card hover>
          <v-card-title>{{ announcement.title }}</v-card-title>
          <v-card-subtitle v-if="announcement.event_date">
            Data do Evento: {{ formatDate(announcement.event_date) }}
          </v-card-subtitle>
          <v-card-text>{{ announcement.content }}</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="warning" variant="text" @click="openModal(announcement)">Editar</v-btn>
            <v-btn color="error" variant="text" @click="deleteAnnouncement(announcement.id)">Excluir</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <div v-else class="text-center mt-16">
      <v-icon size="64" color="grey-lighten-1">mdi-bell-off-outline</v-icon>
      <p class="text-h6 text-grey-darken-1 mt-4">Nenhum anúncio encontrado.</p>
      <p class="text-body-1 text-grey">Parece que ainda não há anúncios disponíveis.</p>
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
const categories = ref([]);
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
    categories.value = categoriesData.value;
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
  console.log("Salvando anúncio:", currentAnnouncement.value);
  try {
    if (currentAnnouncement.value.id) {
      await asyncUseApi(`/warnings/${currentAnnouncement.value.id}`, {
        method: "PUT",
        body: currentAnnouncement.value,
      });
    } else {
      useApi("/warnings/", {
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
  categories.value.map((cat) => ({
    label: cat.name,
    value: cat.id,
  }))
);

onMounted(fetchAnnouncements);
</script>
