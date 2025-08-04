# 📄 Contract API

Este projeto foi criado como requisito de um teste técnico para o cargo de Desenvolvedor **Back-End Python especialista em Inteligência Artificial**.

Trata-se de uma API RESTful construída com **FastAPI** que permite o upload de contratos em formato `.pdf` ou `.docx`, processa o texto utilizando uma API de IA (ex: Gemini) e armazena os dados extraídos em um banco de dados relacional para consulta posterior. Todos os endpoints são protegidos por autenticação JWT.

---

## ✨ Funcionalidades

- 🔐 Login e autenticação via JWT (endpoint `/login`)
    - Credenciais padrão → admin:admin
- 📤 Upload de contratos (endpoint `/contracts/upload`)
- 📄 Processamento com IA (nome das partes, valores, vigência etc.)
- 🗃️ Armazenamento em banco SQLite
- 🔎 Consulta de contratos por nome do arquivo (`/contracts/{filename}`)
- 🐳 Suporte a Docker
- 🧪 Estrutura básica para testes automatizados

---

## ⚙️ Requisitos

- Python 3.10+
- Docker (opcional)

---

## 🚀 Utilização com Docker (recomendado)

### 1. Clonar o projeto e acessar a pasta

```bash
git clone https://github.com/jovemadulto/contract_api.git
cd contract_api
```

### 2. Criar o arquivo `.env` com sua chave da API Gemini (opcional)

A chave API da Gemini deve ser gerada através da plataforma do [Google AI Studio](https://aistudio.google.com/apikey)


```env
GEMINI_API_KEY=sua-chave-aqui
```

### 3. Rodar com Docker Compose

O serviço é inicializado com o nome `api` no Docker.

```bash
docker-compose up api
```

Acesse a API em: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Rodar os testes com Docker Compose

```bash
docker-compose up test --build
```

---

## 🐍 Utilização com ambiente virtual Python (não recomendado)

### 1. Clonar o projeto e acessar a pasta

```bash
git clone https://github.com/jovemadulto/contract_api.git
cd contract_api
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate.bat   # Windows
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Criar o arquivo `.env` com sua chave da API Gemini

A chave API da Gemini deve ser gerada através da plataforma do [Google AI Studio](https://aistudio.google.com/apikey)

```env
GEMINI_API_KEY=sua-chave-aqui
```

### 5. Rodar a aplicação

```bash
uvicorn app.main:app --reload
```

Acesse a API em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Testes

Estrutura de testes presente na pasta `/tests`. Para rodar:

```bash
pytest
```

---

## 📦 Estrutura do projeto

```
contract_api/
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── contracts.py
│   ├── ai_service.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   └── test_auth.py
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```
