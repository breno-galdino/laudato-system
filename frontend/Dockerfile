ARG NODE_VERSION=20.18.0

# Etapa base com dependências
FROM node:${NODE_VERSION}-slim as base

ENV NODE_ENV=development

WORKDIR /app

# Copia os arquivos de dependência e instala
COPY package*.json ./
RUN npm install

# Copia o restante do projeto
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
