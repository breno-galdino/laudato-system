<template>
    <v-card height="100vh">
        <n-color-picker />
    </v-card>
</template>
<script setup>
    const { data, status, error, refresh } = await useApi('/', { cache: 'no-cache' })
</script>