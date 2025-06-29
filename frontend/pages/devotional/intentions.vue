
<template>
  <div class="bg-white min-h-screen py-12">
    <div class="container mx-auto px-4">
      <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Intenções de Missa</h1>
      <div class="grid md:grid-cols-2 gap-12">
        <div>
          <MassIntentionForm />
        </div>
        <div>
          <h2 class="text-2xl font-bold text-gray-800 mb-4">Intenções Enviadas</h2>
          <div class="space-y-4">
            <div v-for="intention in intentions" :key="intention.id" class="bg-gray-100 p-4 rounded-lg shadow-sm">
              <p class="font-semibold">{{ intention.name }}</p>
              <p class="text-gray-600">{{ intention.intention }}</p>
              <p class="text-sm text-gray-500 text-right">{{ intention.status }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import MassIntentionForm from '~/components/MassIntentionForm.vue';

const intentions = ref([
  { id: 1, name: 'João da Silva', intention: 'Pela saúde da minha família', status: 'Aprovação Pendente' },
  { id: 2, name: 'Maria Souza', intention: 'Pelas almas do purgatório', status: 'Aprovada' },
]);
</script>
