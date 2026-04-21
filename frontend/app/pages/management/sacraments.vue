<template>
  <v-container>
    <!-- Header -->
    <v-row justify="space-between" align="center" class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Registros de Sacramentos</h1>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" prepend-icon="mdi-plus" :loading="loading" @click="openModal()">
          Novo Registro
        </v-btn>
      </v-col>
    </v-row>

    <!-- Filtro por tipo -->
    <v-row class="mb-4">
      <v-col cols="12" sm="6" md="4">
        <v-select
          v-model="filterType"
          :items="typeOptions"
          item-title="label"
          item-value="value"
          label="Filtrar por tipo"
          prepend-inner-icon="mdi-filter-outline"
          variant="outlined"
          density="compact"
          clearable
          @update:model-value="fetchSacraments"
        />
      </v-col>
    </v-row>

    <!-- Tabela -->
    <v-card v-if="sacraments.length > 0" variant="outlined" rounded="lg">
      <v-table>
        <thead>
          <tr>
            <th>Tipo</th>
            <th>Pessoa</th>
            <th>Data do Sacramento</th>
            <th>Celebrante</th>
            <th>Nº Certidão</th>
            <th class="text-end">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in sacraments" :key="s.id">
            <td>
              <v-chip :color="typeColor(s.sacrament_type)" size="small" variant="tonal">
                <v-icon start size="small">{{ typeIcon(s.sacrament_type) }}</v-icon>
                {{ typeLabel(s.sacrament_type) }}
              </v-chip>
            </td>
            <td>
              <div class="font-weight-medium">{{ s.person_name }}</div>
              <div v-if="s.person_dob" class="text-caption text-grey">
                Nasc: {{ formatDate(s.person_dob) }}
              </div>
            </td>
            <td>{{ formatDate(s.sacrament_date) }}</td>
            <td>{{ s.officiant || '—' }}</td>
            <td>{{ s.certificate_number || '—' }}</td>
            <td class="text-end">
              <v-btn icon size="small" variant="text" color="warning" @click="openModal(s)">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon size="small" variant="text" color="error" :loading="deletingId === s.id" @click="confirmDelete(s)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>

    <div v-else-if="!loading" class="text-center my-16">
      <v-icon size="64" color="grey-lighten-1">mdi-church</v-icon>
      <p class="text-h6 text-grey-darken-1 mt-4">Nenhum sacramento registrado.</p>
      <p class="text-body-1 text-grey">Clique em "Novo Registro" para adicionar.</p>
    </div>

    <!-- Modal: Criar / Editar -->
    <n-modal
      v-model:show="showModal"
      preset="dialog"
      :title="form.id ? 'Editar Registro' : 'Novo Registro de Sacramento'"
      style="max-width: 600px"
    >
      <n-form :model="form" label-placement="top">
        <n-form-item label="Tipo de Sacramento" required>
          <n-select
            v-model:value="form.sacrament_type"
            :options="typeOptions"
            label-field="label"
            value-field="value"
            placeholder="Selecione o tipo"
          />
        </n-form-item>

        <n-form-item label="Nome da Pessoa" required>
          <n-input v-model:value="form.person_name" placeholder="Nome completo" />
        </n-form-item>

        <n-grid :cols="2" :x-gap="12">
          <n-form-item-gi label="Data de Nascimento">
            <n-date-picker
              v-model:value="form.person_dob"
              type="date"
              clearable
              style="width: 100%"
              format="dd/MM/yyyy"
            />
          </n-form-item-gi>
          <n-form-item-gi label="Data do Sacramento" required>
            <n-date-picker
              v-model:value="form.sacrament_date"
              type="date"
              clearable
              style="width: 100%"
              format="dd/MM/yyyy"
            />
          </n-form-item-gi>
        </n-grid>

        <n-form-item label="Celebrante (Padre)">
          <n-input v-model:value="form.officiant" placeholder="Nome do padre" />
        </n-form-item>

        <!-- Padrinho / Madrinha (batismo e crisma) -->
        <template v-if="['batismo', 'crisma'].includes(form.sacrament_type)">
          <n-grid :cols="2" :x-gap="12">
            <n-form-item-gi label="Padrinho">
              <n-input v-model:value="form.godfather" placeholder="Nome do padrinho" />
            </n-form-item-gi>
            <n-form-item-gi label="Madrinha">
              <n-input v-model:value="form.godmother" placeholder="Nome da madrinha" />
            </n-form-item-gi>
          </n-grid>
        </template>

        <!-- Testemunhas (matrimônio) -->
        <template v-if="form.sacrament_type === 'matrimonio'">
          <n-grid :cols="2" :x-gap="12">
            <n-form-item-gi label="1ª Testemunha">
              <n-input v-model:value="form.witness1" placeholder="Nome da testemunha" />
            </n-form-item-gi>
            <n-form-item-gi label="2ª Testemunha">
              <n-input v-model:value="form.witness2" placeholder="Nome da testemunha" />
            </n-form-item-gi>
          </n-grid>
        </template>

        <n-form-item label="Número da Certidão">
          <n-input v-model:value="form.certificate_number" placeholder="Ex: 123/2025" />
        </n-form-item>

        <n-form-item label="Observações">
          <n-input v-model:value="form.observations" type="textarea" placeholder="Observações adicionais..." />
        </n-form-item>
      </n-form>

      <template #action>
        <n-button @click="showModal = false">Cancelar</n-button>
        <n-button type="primary" :loading="saving" :disabled="!form.sacrament_type || !form.person_name || !form.sacrament_date" @click="saveSacrament">
          Salvar
        </n-button>
      </template>
    </n-modal>
  </v-container>
</template>

<script setup>
const sacraments = ref([])
const loading = ref(false)
const saving = ref(false)
const deletingId = ref(null)
const showModal = ref(false)
const filterType = ref(null)

const emptyForm = () => ({
  id: null,
  sacrament_type: null,
  person_name: '',
  person_dob: null,
  sacrament_date: null,
  officiant: '',
  godfather: '',
  godmother: '',
  witness1: '',
  witness2: '',
  certificate_number: '',
  observations: '',
})

const form = ref(emptyForm())

const typeOptions = [
  { label: 'Batismo', value: 'batismo' },
  { label: 'Primeira Eucaristia', value: 'eucaristia' },
  { label: 'Crisma', value: 'crisma' },
  { label: 'Matrimônio', value: 'matrimonio' },
  { label: 'Ordenação', value: 'ordenacao' },
  { label: 'Unção dos Enfermos', value: 'uncao' },
  { label: 'Penitência / Confissão', value: 'penitencia' },
]

const typeLabel = (type) => typeOptions.find(t => t.value === type)?.label ?? type

const typeColor = (type) => ({
  batismo: 'blue',
  eucaristia: 'amber',
  crisma: 'red',
  matrimonio: 'pink',
  ordenacao: 'purple',
  uncao: 'teal',
  penitencia: 'green',
}[type] ?? 'grey')

const typeIcon = (type) => ({
  batismo: 'mdi-water',
  eucaristia: 'mdi-bread-slice',
  crisma: 'mdi-fire',
  matrimonio: 'mdi-ring',
  ordenacao: 'mdi-cross',
  uncao: 'mdi-bottle-tonic',
  penitencia: 'mdi-hands-pray',
}[type] ?? 'mdi-church')

const fetchSacraments = async () => {
  loading.value = true
  try {
    const params = filterType.value ? `?sacrament_type=${filterType.value}` : ''
    const { data } = await asyncUseApi(`/sacraments/${params}`)
    sacraments.value = data.value ?? []
  } catch (e) {
    console.error('Erro ao buscar sacramentos:', e)
  } finally {
    loading.value = false
  }
}

const openModal = (sacrament = null) => {
  if (sacrament) {
    form.value = {
      ...sacrament,
      person_dob: sacrament.person_dob ? new Date(sacrament.person_dob).getTime() : null,
      sacrament_date: sacrament.sacrament_date ? new Date(sacrament.sacrament_date).getTime() : null,
    }
  } else {
    form.value = emptyForm()
  }
  showModal.value = true
}

const toDateString = (ts) => {
  if (!ts) return null
  const d = new Date(ts)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const saveSacrament = async () => {
  saving.value = true
  try {
    const body = {
      sacrament_type: form.value.sacrament_type,
      person_name: form.value.person_name,
      person_dob: toDateString(form.value.person_dob),
      sacrament_date: toDateString(form.value.sacrament_date),
      officiant: form.value.officiant || null,
      godfather: form.value.godfather || null,
      godmother: form.value.godmother || null,
      witness1: form.value.witness1 || null,
      witness2: form.value.witness2 || null,
      certificate_number: form.value.certificate_number || null,
      observations: form.value.observations || null,
    }

    if (form.value.id) {
      await asyncUseApi(`/sacraments/${form.value.id}`, { method: 'PUT', body })
      message.success('Registro atualizado.')
    } else {
      await asyncUseApi('/sacraments/', { method: 'POST', body })
      message.success('Sacramento registrado com sucesso.')
    }

    showModal.value = false
    await fetchSacraments()
  } catch (e) {
    message.error('Erro ao salvar registro.')
    console.error(e)
  } finally {
    saving.value = false
  }
}

const confirmDelete = (sacrament) => {
  dialog.warning({
    title: 'Excluir registro',
    content: `Deseja excluir o registro de ${typeLabel(sacrament.sacrament_type)} de ${sacrament.person_name}?`,
    positiveText: 'Sim, excluir',
    negativeText: 'Cancelar',
    draggable: true,
    onPositiveClick: async () => {
      deletingId.value = sacrament.id
      try {
        await asyncUseApi(`/sacraments/${sacrament.id}`, { method: 'DELETE' })
        message.success('Registro excluído.')
        await fetchSacraments()
      } catch (e) {
        message.error('Erro ao excluir registro.')
      } finally {
        deletingId.value = null
      }
    },
    onNegativeClick: () => message.info('Ação cancelada.'),
  })
}

const formatDate = (d) => {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('pt-BR')
}

onMounted(fetchSacraments)
</script>
