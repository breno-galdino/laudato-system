<template>
    <v-container class="py-10">
        <!-- Header -->
        <n-h1 align="center" class="mb-10 font-bold text-primary">
            Gestão de Assignments
        </n-h1>

        <!-- Alternar entre lista ou calendário -->
        <div class="flex justify-end mb-4">
            <n-button-group>
                <n-button @click="viewMode = 'list'" :type="viewMode === 'list' ? 'primary' : 'default'">
                    Lista
                </n-button>
                <n-button @click="viewMode = 'calendar'" :type="viewMode === 'calendar' ? 'primary' : 'default'">
                    Calendário
                </n-button>
            </n-button-group>
        </div>

        <!-- Lista de Missas -->
        <div v-if="viewMode === 'list'">
            <v-expansion-panels variant="accordion">
                <v-expansion-panel v-for="celebration in celebrations" :key="celebration.id">
                    <v-expansion-panel-title>
                        {{ celebration.title }} - {{ formatDate(celebration.date) }}
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <v-list>
                            <v-list-item v-for="assignment in celebration.assignments" :key="assignment.id">
                                <v-list-item-title>
                                    {{ getUserName(assignment.userId) }} -
                                    <span class="text-primary">{{ getRoleName(assignment.roleId) }}</span>
                                </v-list-item-title>
                                <template #append>
                                    <n-button text type="error" @click="removeAssignment(assignment)">
                                        Remover
                                    </n-button>
                                </template>
                            </v-list-item>
                        </v-list>
                        <n-button type="primary" secondary @click="openAddAssignment(celebration)">
                            Adicionar Pessoa
                        </n-button>
                    </v-expansion-panel-text>
                </v-expansion-panel>
            </v-expansion-panels>
        </div>

        <!-- Calendário (simplificado com Vuetify v-calendar) -->
        <div v-else>
            <n-calendar v-model:value="value" #="{ year, month, date }" :is-date-disabled="isDateDisabled"
                @update:value="handleUpdateValue">
                {{ year }}-{{ month }}-{{ date }}
            </n-calendar>
        </div>

        <!-- Modal para Adicionar Assignment -->
        <n-modal v-model:show="showModal" preset="dialog" title="Adicionar Assignment">
            <n-form :model="form" label-placement="top">
                <n-form-item label="Usuário">
                    <n-select v-model:value="form.userId" :options="userOptions" placeholder="Selecione o usuário" />
                </n-form-item>
                <n-form-item label="Função">
                    <n-select v-model:value="form.roleId" :options="roleOptions" placeholder="Selecione a função" />
                </n-form-item>
            </n-form>
            <template #action>
                <n-button type="primary" @click="addAssignment">Salvar</n-button>
                <n-button @click="showModal = false">Cancelar</n-button>
            </template>
        </n-modal>
    </v-container>
</template>

<script setup>
    // --- Dados mockados (substituir por GraphQL / REST API) ---
    const celebrations = ref([
        {
            id: 1,
            title: "Missa das 10h",
            date: "2025-08-28",
            assignments: [
                { id: 1, userId: "1", roleId: 1 },
                { id: 2, userId: "2", roleId: 3 }
            ]
        },
        {
            id: 2,
            title: "Missa das 18h",
            date: "2025-08-29",
            assignments: []
        }
    ])

    const userOptions = [
        { label: "Maria Silva", value: "1" },
        { label: "João Santos", value: "2" },
        { label: "Carlos Oliveira", value: "3" }
    ]

    const roleOptions = [
        { label: "Padre", value: 1 },
        { label: "Músico", value: 2 },
        { label: "Leitor", value: 3 },
        { label: "Animador", value: 4 }
    ]

    // --- State ---
    const viewMode = ref("list")
    const showModal = ref(false)
    const currentCelebration = ref(null)
    const form = ref({ userId: null, roleId: null })
    const calendarDate = ref(new Date().toISOString().substring(0, 10))

    // --- Calendar events ---
    const calendarEvents = celebrations.value.map(c => ({
        name: c.title,
        start: c.date,
        color: "blue",
        data: c
    }))

    // --- Helpers ---
    const getUserName = (id) => userOptions.find(u => u.value === id)?.label || "Desconhecido"
    const getRoleName = (id) => roleOptions.find(r => r.value === id)?.label || "Sem função"
    const formatDate = (d) => new Date(d).toLocaleDateString("pt-BR")

    // --- Actions ---
    const openAddAssignment = (celebration) => {
        currentCelebration.value = celebration
        form.value = { userId: null, roleId: null }
        showModal.value = true
    }

    const addAssignment = () => {
        if (!currentCelebration.value) return
        currentCelebration.value.assignments.push({
            id: Date.now(),
            userId: form.value.userId,
            roleId: form.value.roleId
        })
        showModal.value = false
    }

    const removeAssignment = (assignment) => {
        const list = currentCelebration.value?.assignments || []
        const idx = list.findIndex(a => a.id === assignment.id)
        if (idx > -1) list.splice(idx, 1)
    }

    const openEditAssignments = (e) => {
        currentCelebration.value = e.event.data
    }
</script>
