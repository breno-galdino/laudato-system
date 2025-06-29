
<template>
  <div class="bg-gray-100 min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-lg">
      <h1 class="text-2xl font-bold text-gray-800 mb-6">Criar Novo Anúncio</h1>
      <form @submit.prevent="submitAnnouncement">
        <div class="mb-4">
          <label for="title" class="block text-gray-700 font-semibold mb-2">Título</label>
          <input type="text" id="title" v-model="title" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600">
        </div>
        <div class="mb-4">
          <label for="description" class="block text-gray-700 font-semibold mb-2">Descrição</label>
          <textarea id="description" v-model="description" rows="4" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"></textarea>
        </div>
        <div class="mb-6">
          <label for="image" class="block text-gray-700 font-semibold mb-2">URL da Imagem</label>
          <input type="text" id="image" v-model="image" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600">
        </div>
        <button type="submit" class="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Publicar Anúncio</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const title = ref('');
const description = ref('');
const image = ref('');

const submitAnnouncement = () => {
  // Lógica para enviar o anúncio
  console.log({ title: title.value, description: description.value, image: image.value });
};
</script>
