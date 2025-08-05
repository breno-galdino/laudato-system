<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Contato</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="bg-white p-6 rounded-lg shadow-lg">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Informações de Contato</h2>
        <p class="text-gray-600 mb-2"><strong>Endereço:</strong> Rua Exemplo, 123, Cidade, Estado</p>
        <p class="text-gray-600 mb-2"><strong>Telefone:</strong> (11) 99999-9999</p>
        <p class="text-gray-600"><strong>Email:</strong> contato@exemplo.com</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-lg">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Envie uma Mensagem</h2>
        <form>
          <div class="mb-4">
            <label for="name" class="block text-gray-700 text-sm font-bold mb-2">Nome:</label>
            <input type="text" id="name" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
          </div>
          <div class="mb-4">
            <label for="email" class="block text-gray-700 text-sm font-bold mb-2">Email:</label>
            <input type="email" id="email" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
          </div>
          <div class="mb-4">
            <label for="message" class="block text-gray-700 text-sm font-bold mb-2">Mensagem:</label>
            <textarea id="message" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"></textarea>
          </div>
          <div class="flex justify-end">
            <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              Enviar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>