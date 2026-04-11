<template>
  <v-container>
    <n-h1 align="center" class="mb-8">Intenções de Missa</n-h1>
    <v-row justify="center" :gutter="48">
      <v-col cols="12" md="6">
        <MassIntentionForm />
      </v-col>
      <v-col cols="12" md="6">
        <n-h2>Intenções Enviadas</n-h2>
        <n-space vertical size="large">
          <v-card v-for="intention in intentions" :key="intention.id" variant="outlined">
            <v-card-title>{{ intention.name }}</v-card-title>
            <v-card-text>{{ intention.intention }}</v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-chip :color="intention.status === 'Aprovada' ? 'success' : 'warning'" label>
                {{ intention.status }}
              </v-chip>
            </v-card-actions>
          </v-card>
        </n-space>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';

const intentions = ref([
  { id: 1, name: 'João da Silva', intention: 'Pela saúde da minha família', status: 'Aprovação Pendente' },
  { id: 2, name: 'Maria Souza', intention: 'Pelas almas do purgatório', status: 'Aprovada' },
]);
</script>