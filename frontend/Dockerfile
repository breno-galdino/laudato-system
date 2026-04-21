ARG NODE_VERSION=20.18.0

# Etapa base com dependências
FROM node:${NODE_VERSION}-slim as base

ENV NODE_ENV=development

WORKDIR /app

# Copia manifests e instala sem rodar postinstall (nuxt prepare
# falha aqui pois o nuxt.config.ts ainda não foi copiado)
COPY package*.json ./
RUN npm install --ignore-scripts

# Copia o projeto completo
COPY . .

# Agora o nuxt.config.ts existe — pode preparar os tipos
RUN npm run postinstall

EXPOSE 3000

CMD ["npm", "run", "dev"]
