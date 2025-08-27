<!-- <template><div>{{users}}</div></template>
<script setup>
import GetCelebrations from '@/queries/schedules.gql'

const { data: users, loading, error } = await useAsyncQuery(GetCelebrations);

</script> -->
<template>
  <n-card title="Criar Assignment" class="max-w-xl mx-auto mt-10 p-6">
    <n-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-placement="top"
      size="large"
    >
      <!-- Celebration -->
      <n-form-item label="Missa" path="celebrationId">
        <n-select
          v-model:value="form.celebrationId"
          :options="celebrationOptions"
          placeholder="Selecione a missa"
        />
      </n-form-item>

      <!-- User -->
      <n-form-item label="Usuário" path="userId">
        <n-select
          v-model:value="form.userId"
          :options="userOptions"
          placeholder="Selecione o usuário"
        />
      </n-form-item>

      <!-- Role -->
      <n-form-item label="Função" path="roleId">
        <n-select
          v-model:value="form.roleId"
          :options="roleOptions"
          placeholder="Selecione a função"
        />
      </n-form-item>

      <!-- Submit -->
      <div class="flex justify-end mt-6">{{ form }}
        <n-button
          type="primary"
          :loading="loading"
          @click="mutate(form)"
        >
          Criar Assignment
        </n-button>
      </div>
    </n-form>
  </n-card>
</template>

<script setup>

// --- GraphQL Mutation ---
const mutation = gql`
  mutation putAssignment($celebrationId: Int!, $userId: UUID!, $roleId: Int!) {
    putAssignment(params: {celebrationId: $celebrationId, userId: $userId, roleId: $roleId}) {
      id
      celebrationId
      userId
      roleId
    }
  }
`;

// --- Form ---
const formRef = ref(null);
const form = ref({
  celebrationId: null,
  userId: null,
  roleId: null
});
const rules = {
  celebrationId: { required: true, message: "Selecione a missa" },
  userId: { required: true, message: "Selecione o usuário" },
  roleId: { required: true, message: "Selecione a função" }
};

// --- Mock options (substituir por API) ---
const celebrationOptions = [
  { label: "Missa das 10h", value: 1 },
  { label: "Missa das 18h", value: 2 }
];
const userOptions = [
  { label: "Maria Silva", value: "6d75635c-9a2d-4858-9a6c-4f04abebd18f" },
  { label: "João Santos", value: "6d75635c-9a2d-4858-9a6c-4f04abebd18f" }
];
const roleOptions = [
  { label: "Padre", value: 1 },
  { label: "Músico", value: 2 },
  { label: "Leitor", value: 3 },
  { label: "Animador", value: 4 }
];

// --- Mutation ---
const loading = ref(false);
const {mutate} = useMutation(mutation);

</script>

<style scoped>
.max-w-xl {
  max-width: 600px;
}
.mx-auto {
  margin-left: auto;
  margin-right: auto;
}
</style>
