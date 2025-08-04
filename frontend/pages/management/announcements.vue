
<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Gerenciar Anúncios</h1>
    <div class="flex justify-end mb-4">
      <button @click="openModal" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Novo Anúncio
      </button>
    </div>
    <div class="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
      <div v-for="announcement in announcements" :key="announcement.id" class="relative">
        <AnnouncementCard :announcement="announcement" />
        <div class="absolute top-2 right-2">
          <button @click="openModal(announcement)" class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-1 px-2 rounded mr-2">
            Editar
          </button>
          <button @click="deleteAnnouncement(announcement.id)" class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded">
            Excluir
          </button>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
              {{ currentAnnouncement.id ? 'Editar Anúncio' : 'Novo Anúncio' }}
            </h3>
            <div class="mt-2">
              <form @submit.prevent="saveAnnouncement">
                <div class="mb-4">
                  <label for="title" class="block text-gray-700 text-sm font-bold mb-2">Título:</label>
                  <input v-model="currentAnnouncement.title" type="text" id="title" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                </div>
                <div class="mb-4">
                  <label for="description" class="block text-gray-700 text-sm font-bold mb-2">Descrição:</label>
                  <textarea v-model="currentAnnouncement.description" id="description" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"></textarea>
                </div>
                <div class="flex justify-end">
                  <button type="button" @click="closeModal" class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded mr-2">
                    Cancelar
                  </button>
                  <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    Salvar
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const announcements = ref([]);
const showModal = ref(false);
const currentAnnouncement = ref({
  id: null,
  title: '',
  description: '',
});

const fetchAnnouncements = async () => {
  try {
    const { data } = await useApi('/warnings');
    announcements.value = data.value;
  } catch (error) {
    console.error('Erro ao buscar anúncios:', error);
  }
};

const openModal = (announcement = null) => {
  if (announcement) {
    currentAnnouncement.value = { ...announcement };
  } else {
    currentAnnouncement.value = { id: null, title: '', description: '' };
  }
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const saveAnnouncement = async () => {
  try {
    if (currentAnnouncement.value.id) {
      await useApi(`/warnings/${currentAnnouncement.value.id}`, {
        method: 'PUT',
        body: JSON.stringify(currentAnnouncement.value),
        headers: {
          'Content-Type': 'application/json'
        }
      });
    } else {
      await useApi('/warnings', {
        method: 'POST',
        body: JSON.stringify(currentAnnouncement.value),
        headers: {
          'Content-Type': 'application/json'
        }
      });
    }
    closeModal();
    fetchAnnouncements();
  } catch (error) {
    console.error('Erro ao salvar anúncio:', error);
  }
};

const deleteAnnouncement = async (id) => {
  try {
    await useApi(`/warnings/${id}`, {
      method: 'DELETE'
    });
    fetchAnnouncements();
  } catch (error) {
    console.error('Erro ao excluir anúncio:', error);
  }
};

onMounted(fetchAnnouncements);
</script>
