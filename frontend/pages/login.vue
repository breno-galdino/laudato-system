<template>
  <v-app>
    <v-main>
      <div class="background-wrapper">
        <div class="auth-wrapper d-flex">
          <!-- Lado Esquerdo -->
          <div class="welcome-side d-flex flex-column align-center justify-center text-center">
            <h2 class="text-white text-h4 font-weight-bold">Bem Vindo!</h2>
            <p class="text-white mt-2">
              Para se manter conectado conosco<br />
              por favor logue com suas informações pessoais.
            </p>
          </div>

          <!-- Lado Direito -->
          <div class="register-side d-flex flex-column align-center justify-center text-center">
            <h2 class="text-primary text-h5 font-weight-bold mb-4">Criar conta</h2>

        

            <v-form @submit.prevent="register" class="w-75">
              <v-text-field
                v-model="newUser.name"
                label="Nome"
                prepend-inner-icon="mdi-account"
                variant="solo-filled"
                hide-details
                class="mb-3"
              />
              <v-text-field
                v-model="newUser.email"
                label="Email"
                prepend-inner-icon="mdi-email"
                variant="solo-filled"
                hide-details
                class="mb-3"
              />
              <v-text-field
                v-model="newUser.password"
                label="Senha"
                type="password"
                prepend-inner-icon="mdi-lock"
                variant="solo-filled"
                hide-details
                class="mb-3"
              />
              <v-btn type="submit" color="primary" class="text-white mt-2" block>
                REGISTRE-SE
              </v-btn>

              <v-btn variant="text" class="mt-4" @click="goToLogin">
                Já tenho uma conta
              </v-btn>
            </v-form>
          </div>
        </div>
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from "vue";

const newUser = ref({
  name:"",
  email:"",
  password:""
})

const register = () => {
  const {data} = useApi("/login",{body:newUser.value})
};

const goToLogin = () => {
  alert("Ir para login...");
};
</script>

<style scoped>
/* Ocupa tela inteira sem scroll */
.background-wrapper {
  position: relative;
  height: 100vh;
  width: 100vw;
  background: url("https://4kwallpapers.com/images/walls/thumbs_3t/13554.jpg") no-repeat center center;
  background-size: cover;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Bloco central */
.auth-wrapper {
  width: 900px;
  height: 500px;
  background-color: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  display: flex;
  position: relative;
  z-index: 1;
}

/* Lado Esquerdo */
.welcome-side {
  background: linear-gradient(135deg, #222831, #393E46);
  width: 50%;
  padding: 40px;
  color: white;
}

/* Lado Direito */
.register-side {
  background-color: #fff;
  width: 50%;
  padding: 40px;
}

/* Ícones sociais */
.social-icon {
  border-radius: 50%;
}
</style>
