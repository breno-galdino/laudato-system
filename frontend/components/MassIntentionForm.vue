<template>
  <v-card class="pa-4">
    <v-card-title class="text-h5">Enviar Intenção de Missa</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="submitIntention">
        <v-text-field v-model="name" label="Seu Nome" required></v-text-field>
        <v-textarea v-model="intention" label="Intenção" rows="4" required></v-textarea>
        <v-btn type="submit" color="primary" block>Enviar Intenção</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
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