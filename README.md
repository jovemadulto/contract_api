# Analisador de Contratos com IA | Biofy

Este projeto é uma aplicação web completa que utiliza Inteligência Artificial Generativa (Google Gemini) para analisar contratos jurídicos. A aplicação é construída com **FastAPI** para o back-end e um front-end **HTML/CSS/JS** integrado, tudo containerizado com **Docker**.

A aplicação permite que um usuário autenticado faça o upload de um documento de contrato (`.pdf` or `.docx`). O back-end extrai o texto, o envia para a IA para análise e, em seguida, armazena e exibe os dados estruturados extraídos, como as partes, obrigações, valores e vigência.

## Features

  * **API Back-end:** API RESTful robusta construída com FastAPI.
  * **Autenticação JWT:** Endpoints protegidos usando autenticação baseada em token JWT (`admin`/`admin`).
  * **Upload de Arquivos:** Aceita arquivos `.pdf` e `.docx` para análise.
  * **Extração de Texto:** Processa PDFs (incluindo leitura de stream de bytes para evitar `FileNotFoundError`) e documentos Word.
  * **Análise com IA:** Integra-se com a API Google Gemini para extrair informações-chave do contrato, formatando a saída como JSON estruturado (incluindo listas para obrigações, partes, etc.).
  * **Banco de Dados:** Armazena os resultados da análise em um banco de dados **SQLite**.
  * **Front-end Integrado:** Um front-end de página única (SPA) servido diretamente pelo FastAPI.
  * **UI Amigável:** O front-end lida com login, upload de arquivos e exibe os resultados da análise em uma lista HTML formatada e fácil de ler, em vez de JSON bruto.
  * **Containerização:** Totalmente configurado para ser construído e executado com **Docker**.

## Tech Stack

  * **Back-end:** FastAPI, Uvicorn
  * **Processamento de Documentos:** PyMuPDF (Fitz), python-docx
  * **Banco de Dados:** SQLAlchemy, SQLite
  * **IA:** Google Generative AI (Gemini)
  * **Autenticação:** PyJWT
  * **Containerização:** Docker
  * **Front-end:** HTML5, CSS3, JavaScript (Vanilla)

-----

## Setup e Execução

Para executar este projeto, você precisará do [Docker](https://www.docker.com/) instalado.

### 1\. Arquivo de Configuração (`.env`)

Crie um arquivo `.env` na raiz do projeto. Este arquivo é crucial para armazenar suas chaves de API e segredos.

```
GEMINI_API_KEY=sua_chave_de_api_do_gemini_aqui
JWT_SECRET_KEY=um_segredo_muito_forte_para_seus_tokens_jwt
```

> **Nota:** O usuário e senha padrão estão codificados em `app/auth.py` como `admin`/`admin`.

### 2\. Construir a Imagem Docker

Abra um terminal na raiz do projeto e execute:

```bash
docker build -t contract-analyzer .
```

### 3\. Executar o Container

Após a construção da imagem, inicie o container:

```bash
docker run -p 8000:8000 --env-file .env contract-analyzer
```

  * `-p 8000:8000`: Mapeia a porta 8000 do seu computador para a porta 8000 dentro do container.
  * `--env-file .env`: Passa com segurança suas variáveis de ambiente para dentro do container.

### 3\.1. Executar o Container com Docker Compose

```bash
# Constrói a imagem (se ainda não existir) e sobe o container
# O -d executa em modo "detached" (em segundo plano)
docker-compose up -d --build
```

### 4\. Acessar a Aplicação

Abra seu navegador e acesse:
**`http://localhost:8000/`**

Você verá a interface de login. Use as credenciais padrão (`admin`/`admin`) para fazer o login e começar a enviar contratos.

-----

## API Endpoints

A aplicação expõe os seguintes endpoints:

  * `GET /`: Serve a aplicação front-end `index.html`.
  * `POST /login`: Recebe `username` e `password` (form-data) e retorna um `access_token` JWT.
  * `POST /contracts/upload`: (Protegido) Recebe um `UploadFile`. Processa o arquivo, o analisa com IA, salva no DB e retorna a análise em JSON.
  * `GET /contracts/{filename}`: (Protegido) Recupera os dados de uma análise de contrato salva pelo nome do arquivo.
  * `GET /docs`: Acessa a documentação interativa da API (Swagger UI).
  * `GET /redoc`: Acessa a documentação alternativa da API (ReDoc).

-----

## Estrutura do projeto

```
contract_api/
├── app/
│   ├── ai_service.py     # Lógica de integração com a IA (Gemini)
│   ├── auth.py           # Funções de autenticação e JWT
│   ├── contracts.py      # Rotas da API para /contracts, lógica de upload e extração
│   ├── database.py       # Configuração do banco de dados (SQLAlchemy + SQLite)
│   ├── main.py           # Ponto de entrada principal do FastAPI (serve o front-end)
│   ├── models.py         # Modelos de dados do SQLAlchemy
│   └── schemas.py        # Modelos de dados do Pydantic (validação de request/response)
│
├── static/
│   └── index.html        # O front-end completo (HTML/CSS/JS)
│
├── tests/
│   └── test_auth.py      #
│
├── .env                  # Armazena variáveis de ambiente de forma segura
├── Dockerfile            # Instruções para construir a imagem Docker
├── docker-compose.yml    # Configurações do Docker Compose
├── requirements.txt      # Dependências Python
└── README.md             # Este arquivo
```
