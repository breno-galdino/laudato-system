
<template>
  <div class="bg-gray-50 font-sans">
    <header class="bg-white shadow-sm">
      <div class="container mx-auto px-6 py-4 flex justify-between items-center">
        <NuxtLink to="/" class="text-2xl font-bold text-gray-800">Laudato System</NuxtLink>
        <nav class="hidden md:flex space-x-8">
          <NuxtLink to="/" class="text-gray-600 hover:text-blue-600">Início</NuxtLink>
          <NuxtLink to="/community" class="text-gray-600 hover:text-blue-600">Comunidade</NuxtLink>
          <NuxtLink to="/devotional" class="text-gray-600 hover:text-blue-600">Devocional</NuxtLink>
          <NuxtLink to="/contact" class="text-gray-600 hover:text-blue-600">Contato</NuxtLink>
        </nav>
        <div class="flex items-center space-x-4">
          <button @click="toggleTheme" class="px-4 py-2 rounded-lg text-gray-600 hover:text-blue-600">
            <Icon name="mdi:theme-light-dark" class="text-2xl" />
          </button>
          <NuxtLink to="/login" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Entrar</NuxtLink>
        </div>
      </div>
    </header>
    <main>
      <slot />
    </main>
    <footer class="bg-gray-800 text-white py-8">
      <div class="container mx-auto px-6 text-center">
        <p>&copy; 2024 Laudato System. Todos os direitos reservados.</p>
        <div class="flex justify-center space-x-6 mt-4">
          <a href="#" class="hover:text-blue-400"><Icon name="mdi:facebook" class="text-2xl" /></a>
          <a href="#" class="hover:text-blue-400"><Icon name="mdi:twitter" class="text-2xl" /></a>
          <a href="#" class="hover:text-blue-400"><Icon name="mdi:instagram" class="text-2xl" /></a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useTheme } from 'vuetify'

const theme = useTheme()

function toggleTheme () {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
}
</script>
