<template>
  <v-card class="pa-4">
    <v-card-title class="text-h5">Enviar Mensagem em Massa</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="sendMessage">
        <v-select
          v-model="recipientGroup"
          :items="recipientGroups"
          label="Grupo de Destinatários"
          required
        ></v-select>
        <v-textarea v-model="message" label="Mensagem" rows="4" required></v-textarea>
        <v-radio-group v-model="channel" inline label="Canal">
          <v-radio label="E-mail" value="email"></v-radio>
          <v-radio label="WhatsApp" value="whatsapp"></v-radio>
        </v-radio-group>
        <v-btn type="submit" color="primary" block>Enviar Mensagem</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref } from 'vue';

const recipientGroup = ref('all');
const message = ref('');
const channel = ref('email');

const recipientGroups = [
  { title: 'Todos os Paroquianos', value: 'all' },
  { title: 'Catequistas', value: 'catechists' },
  { title: 'Voluntários', value: 'volunteers' },
];

const sendMessage = () => {
  // Lógica para enviar a mensagem
  console.log({ recipientGroup: recipientGroup.value, message: message.value, channel: channel.value });
};
</script>