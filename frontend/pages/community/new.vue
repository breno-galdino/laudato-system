<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <v-card class="pa-4">
          <v-card-title class="text-h5">Criar Novo Anúncio</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="submitAnnouncement">
              <v-text-field
                v-model="title"
                label="Título"
                required
              ></v-text-field>
              <v-textarea
                v-model="description"
                label="Descrição"
                rows="4"
                required
              ></v-textarea>
              <v-text-field
                v-model="image"
                label="URL da Imagem"
              ></v-text-field>
              <v-btn type="submit" color="primary" block>Publicar Anúncio</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
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