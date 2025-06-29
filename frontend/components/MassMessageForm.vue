
<template>
  <div class="bg-white p-8 rounded-lg shadow-md">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Enviar Mensagem em Massa</h2>
    <form @submit.prevent="sendMessage">
      <div class="mb-4">
        <label for="recipientGroup" class="block text-gray-700 font-semibold mb-2">Grupo de Destinatários</label>
        <select id="recipientGroup" v-model="recipientGroup" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600">
          <option value="all">Todos os Paroquianos</option>
          <option value="catechists">Catequistas</option>
          <option value="volunteers">Voluntários</option>
        </select>
      </div>
      <div class="mb-4">
        <label for="message" class="block text-gray-700 font-semibold mb-2">Mensagem</label>
        <textarea id="message" v-model="message" rows="4" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"></textarea>
      </div>
      <div class="mb-6">
        <label class="block text-gray-700 font-semibold mb-2">Canal</label>
        <div class="flex space-x-4">
          <label class="flex items-center">
            <input type="radio" name="channel" value="email" v-model="channel" class="form-radio text-blue-600">
            <span class="ml-2">E-mail</span>
          </label>
          <label class="flex items-center">
            <input type="radio" name="channel" value="whatsapp" v-model="channel" class="form-radio text-blue-600">
            <span class="ml-2">WhatsApp</span>
          </label>
        </div>
      </div>
      <button type="submit" class="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Enviar Mensagem</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const recipientGroup = ref('all');
const message = ref('');
const channel = ref('email');

const sendMessage = () => {
  // Lógica para enviar a mensagem
  console.log({ recipientGroup: recipientGroup.value, message: message.value, channel: channel.value });
};
</script>
