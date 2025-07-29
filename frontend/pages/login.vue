<template>
  <v-app>
    <v-main>
      <div class="background-wrapper">
        <div class="auth-wrapper d-flex text-center">
          <!-- Lado Esquerdo -->
            <div class="welcome-side flex flex-col items-center justify-center text-center h-full">
            <h2 class="text-white text-3xl font-bold">Bem Vindo!</h2>
            <p class="text-white mt-2">
              Para se manter conectado conosco<br />
              por favor acesse sua conta.
            </p>
            </div>

          <!-- Lado Direito -->
          <div class="register-side flex flex-col items-center justify-center text-center">
            <img src="/logo.png" alt="Logotipo" class="mb-4 w-32 h-24">

            <v-form @submit.prevent="register" class="w-75">
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
                ENTRAR
              </v-btn>

                  <div class="mt-4 text-center">
                  <span class="text-gray-600">Não tem uma conta?</span>
                  <a href="/register" class="ml-1 text-primary font-semibold hover:underline">
                    Registre-se
                  </a>
                  </div>
            </v-form>
          </div>
        </div>
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
const newUser = ref({
  name:"",
  email:"",
  password:""
})

const register = () => {
  const {data} = useApi("/login",{body:newUser.value})
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
