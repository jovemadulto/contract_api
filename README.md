# 📄 Contract API

Este projeto foi criado como requisito de um teste técnico para o cargo de Desenvolvedor **Back-End Python especialista em Inteligência Artificial**.

Trata-se de uma API RESTful construída com **FastAPI** que permite o upload de contratos em formato `.pdf` ou `.docx`, processa o texto utilizando uma API de IA (ex: Gemini) e armazena os dados extraídos em um banco de dados relacional para consulta posterior. Todos os endpoints são protegidos por autenticação JWT.

---

## ✨ Funcionalidades

- 🔐 Login e autenticação via JWT (`/login`)
- 📤 Upload de contratos (`/contracts/upload`)
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
git clone <repo-url>
cd contract_api
```

### 2. Criar o arquivo `.env` com sua chave da API Gemini (opcional)

```env
GEMINI_API_KEY=sua-chave-aqui
```

### 3. Rodar com Docker Compose

```bash
docker-compose up --build
```

Acesse a API em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐍 Utilização com ambiente virtual Python

### 1. Clonar o projeto e acessar a pasta

```bash
git clone <repo-url>
cd contract_api
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Criar o arquivo `.env` com sua chave da API Gemini

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

## 📦 Estrutura

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
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---