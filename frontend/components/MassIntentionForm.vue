
<template>
  <div class="bg-gray-100 p-8 rounded-lg shadow-md">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Enviar Intenção de Missa</h2>
    <form @submit.prevent="submitIntention">
      <div class="mb-4">
        <label for="name" class="block text-gray-700 font-semibold mb-2">Seu Nome</label>
        <input type="text" id="name" v-model="name" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-600">
      </div>
      <div class="mb-4">
        <label for="intention" class="block text-gray-700 font-semibold mb-2">Intenção</label>
        <textarea id="intention" v-model="intention" rows="4" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-600"></textarea>
      </div>
      <button type="submit" class="w-full bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700">Enviar Intenção</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const name = ref('');
const intention = ref('');

const submitIntention = () => {
  // Lógica para enviar a intenção
  console.log({ name: name.value, intention: intention.value });
};
</script>
