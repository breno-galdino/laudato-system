<template>
  <v-container class="text-center">
    <n-h1 class="mb-2">Acenda uma Vela Virtual</n-h1>
    <p class="text-h6 font-weight-light mb-8">Ofereça uma oração e acenda uma vela como símbolo de sua fé.</p>
    <v-row>
      <v-col v-for="candle in candles" :key="candle.id" cols="6" sm="4" md="3" lg="2">
        <VirtualCandle :candle="candle" />
      </v-col>
    </v-row>
    <v-btn @click="addCandle" color="primary" size="large" class="mt-8">Acender uma Nova Vela</v-btn>
  </v-container>
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