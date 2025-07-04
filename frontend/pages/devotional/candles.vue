
<template>
  <div class="bg-white min-h-screen py-12">
    <div class="container mx-auto px-4 text-center">
      <h1 class="text-4xl font-bold text-gray-800 mb-2">Acenda uma Vela Virtual</h1>
      <p class="text-gray-600 mb-8">Ofereça uma oração e acenda uma vela como símbolo de sua fé.</p>
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6 mb-8">
        <VirtualCandle v-for="candle in candles" :key="candle.id" :candle="candle" />
      </div>
      <button @click="addCandle" class="bg-yellow-600 text-white px-6 py-3 rounded-lg hover:bg-yellow-700">Acender uma Nova Vela</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import VirtualCandle from '~/components/VirtualCandle.vue';

const candles = ref([
  { id: 1, intention: 'Pela paz no mundo' },
  { id: 2, intention: 'Em ação de graças' },
]);

const addCandle = () => {
  const intention = prompt('Qual é a sua intenção?');
  if (intention) {
    candles.value.push({ id: Date.now(), intention });
  }
};
</script>
