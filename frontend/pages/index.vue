<template>
    <div>
        <v-btn @click="refresh">Refresh</v-btn>
        {{ status }}{{ data ?? "WAITANDO" }}
    </div>
</template>
<script setup>
    const { data, status, error, refresh } = await useApi('/', {cache: 'no-cache'})
</script>