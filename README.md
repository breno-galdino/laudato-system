# 🙏 Sistema Paroquial Integrado - Gestão e Informações da Igreja

**Versão Inicial - Em Desenvolvimento**

Este projeto tem como objetivo facilitar a **gestão e comunicação** de paróquias e comunidades católicas por meio de uma plataforma web integrada, moderna e acessível.

## ✨ Visão Geral

O Sistema Paroquial Integrado foi idealizado para servir como uma ferramenta digital de apoio à vida eclesial, abrangendo **pastorais, sacramentos, catequese, eventos, liturgia e muito mais**. Ele permitirá uma administração mais eficiente, participativa e transparente da paróquia.

## 🔧 Tecnologias Planejadas

- **Frontend**: Nuxt 3 / Vue 3 + JavaScript  
- **Backend**: FastAPI + SQLAlchemy / SQLModel  
- **Banco de Dados**: PostgreSQL  
- **Autenticação**: JWT com permissões por papel (admin, coordenador, fiel, visitante)  
- **Integrações Futuras**: WhatsApp API, sistemas de pagamento (Pix, PagSeguro)

---

## 📌 Módulos Futuramente Desenvolvidos

### ✅ 1. Escalas de Missas e Liturgia
- Cadastro e edição de celebrações
- Criação de escalas para leitores, ministros, músicos etc.
- Envio automático de lembretes para os escalados

### ✅ 2. Gestão de Usuários e Permissões
- Cadastro de paroquianos com níveis de acesso
- Login seguro (e-mail, CPF ou matrícula)
- Edição de perfis e atribuição a pastorais

### ✅ 3. Agenda e Eventos Paroquiais
- Calendário geral com eventos, missas e reuniões
- Reservas de espaços físicos da paróquia
- Notificações e lembretes por e-mail ou WhatsApp

### ✅ 4. Biblioteca de Documentos e Conteúdo
- Upload e categorização de documentos eclesiais
- Catequese online com PDFs, vídeos e textos
- Área para artigos e reflexões doutrinárias

### ✅ 5. Módulo Financeiro e Doações
- Controle de dízimos e campanhas
- Relatórios financeiros para coordenações
- Pagamento online (Pix, boletos, cartões)

### ✅ 6. Catequese e Formação Cristã
- Cadastro de turmas, catequizandos e catequistas
- Controle de presença
- Emissão automática de certificados (PDF)

### ✅ 7. Comunicação com a Comunidade
- Mural de avisos e notícias
- Envio em massa de mensagens via e-mail ou WhatsApp
- Integração com redes sociais (Instagram/Facebook)

### ✅ 8. Cadastro de Sacramentos
- Registro e histórico sacramental de cada fiel
- Emissão de certidões (batismo, casamento, crisma)
- Busca e emissão rápida de segunda via

### ✅ 9. Gestão de Pastorais e Movimentos
- Cadastro de grupos e coordenações
- Agendamento de reuniões
- Registro de participantes

### ✅ 10. Módulo Devocional
- Intenções de missa online (com aprovação do pároco)
- Acendimento de velas virtuais com intenções
- Áudio/orientações para novenas e orações

---

## 🚀 Roadmap de Desenvolvimento (Etapas)

| Etapa | Módulos | Status |
|-------|---------|--------|
| Fase 1 | Gestão de usuários, escalas litúrgicas, agenda e avisos | 🔄 Em andamento |
| Fase 2 | Catequese, sacramentos, biblioteca e documentos | ⏳ Planejado |
| Fase 3 | Financeiro, doações e módulo devocional | ⏳ Planejado |
| Fase 4 | Integração com WhatsApp, pagamentos e geração de relatórios | ⏳ Planejado |
| Fase 5 | Painel administrativo com analytics e notificações | ⏳ Planejado |

---

## 📁 Estrutura Inicial do Projeto (Proposta)

```plaintext
parish-system/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   └── main.py
├── frontend/
│   └── nuxt-app/
│       ├── components/
│       ├── pages/
│       ├── plugins/
│       └── stores/
└── README.md
