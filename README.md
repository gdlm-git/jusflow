# JusFlow

Sistema de gestão de clientes desenvolvido em **Python + Flask** para projeto acadêmico da **Faculdade Impacta**.

## Descrição

O **JusFlow** é um sistema web simples para gerenciamento de clientes, permitindo cadastrar, editar, buscar e excluir registros de forma organizada.

O sistema foi desenvolvido com foco em demonstrar conceitos de **CRUD, autenticação básica e organização de projeto web utilizando Flask**.

---

##  Funcionalidades

- Login de acesso ao sistema
- Cadastro de clientes
- Listagem de clientes
- Edição de clientes
- Exclusão de clientes
- Busca por nome ou CPF
- Validação para evitar CPF duplicado
- Mensagens de sucesso ao salvar alterações

- Cadastro de processos vinculado a cliente existente (via CPF)
- Cadastro de processo direto pelo cliente
- Listagem de processos
- Edição de processos
- Exclusão de processos
- Validação de cliente existente ao cadastrar processo
- Landing Page pública para solicitação de atendimento jurídico
- Captação de clientes via formulário online
- Cadastro automático de leads na base de clientes
- Definição automática do status inicial do cliente como Novo
- Integração da Landing Page com o backend Flask
- Persistência dos dados captados no PostgreSQL (Supabase)
- Feedback visual de sucesso após envio da solicitação
---

##  Tecnologias utilizadas

- Python
- Flask
- PostgreSQL (Supabase)
- HTML
- Bootstrap
- Git
- GitHub

---

## 📂 Estrutura do projeto
- `templates/landing_page.html`: página pública de captação de clientes
- `static/imagens/`: pasta de imagens utilizadas na Landing Page
---