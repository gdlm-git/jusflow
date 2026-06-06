# JusFlow

Sistema de gestão de clientes e processos jurídicos desenvolvido em **Python + Flask** para projeto acadêmico da **Faculdade Impacta**.

---

# Descrição

O **JusFlow** é um sistema web voltado para escritórios jurídicos, permitindo o gerenciamento de clientes, processos e captação de novos atendimentos através de uma Landing Page pública.

O sistema foi desenvolvido para demonstrar conceitos de:

- CRUD completo
- Relacionamento entre entidades
- Autenticação básica
- Persistência em banco de dados PostgreSQL
- Dashboard com indicadores e filtros
- Arquitetura web utilizando Flask

---

# Funcionalidades

## Autenticação

- Login de acesso ao sistema
- Controle de sessão
- Logout

## Gestão de Clientes

- Cadastro de clientes
- Edição de clientes
- Exclusão de clientes
- Busca por nome ou CPF
- Validação de CPF duplicado
- Controle de status do cliente

## Gestão de Processos

- Cadastro de processos
- Vinculação de processo ao cliente
- Edição de processos
- Exclusão de processos
- Consulta de processos

## Landing Page de Captação

- Página pública de solicitação de atendimento
- Cadastro automático de novos clientes
- Definição automática do status "Novo"
- Integração com banco de dados PostgreSQL
- Feedback visual após envio do formulário

## Dashboard Gerencial

- Total de clientes cadastrados
- Total de processos cadastrados
- Total de leads captados
- Total de processos em andamento
- Filtro por tipo de processo
- Filtro por status
- Filtro por período
- Gráfico de clientes por status
- Gráfico de processos por status
- Gráfico de processos por tipo
- Gráfico de valor da causa por tipo
- Exportação de dados em CSV

---

# Tecnologias Utilizadas

- Python
- Flask
- PostgreSQL (Supabase)
- HTML5
- CSS3
- Bootstrap
- Chart.js
- Git
- GitHub

---

# Estrutura do Projeto

## Templates

- `login.html` → tela de autenticação
- `home.html` → menu principal
- `clientes.html` → listagem de clientes
- `cadastro.html` → cadastro de clientes
- `editar_cliente.html` → edição de clientes
- `detalhe_cliente.html` → detalhes do cliente

- `processos.html` → listagem de processos
- `cadastro_processo.html` → cadastro de processos
- `editar_processo.html` → edição de processos
- `detalhe_processo.html` → detalhes do processo

- `landing_page.html` → página pública de captação
- `dashboard.html` → painel gerencial e relatórios

## Backend

- `app.py` → regras de negócio, rotas e integração com banco

## Arquivos Estáticos

- `static/imagens/` → imagens utilizadas pela Landing Page

---

# Modelo de Dados

## Cliente

- Nome
- CPF
- Telefone
- E-mail
- Tipo de causa
- Status

## Processo

- Número do processo
- Descrição
- Data de abertura
- Status
- Tipo de processo
- Valor da causa
- Vara
- Advogado responsável

---

# Autor

Projeto desenvolvido por **Gedeão Lima** para a disciplina:

**Software Product: Analysis, Specification, Project & Implementation**

Faculdade Impacta