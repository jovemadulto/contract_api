from .auth import authenticate_user, create_access_token
from .contracts import router as contracts_router
from .database import Base, engine
from .schemas import Token
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

Base.metadata.create_all(bind=engine)

application_description = """
Esta aplicação facilita a análise de contratos jurídicos utilizando o auxílio de inteligência artificial generativa.

Por meio desta interface o usuário pode fazer o upload de documentos nos formatos .pdf e .docx para serem analisados.

São retornados detalhes críticos dos contratos como:
- As partes envolvidas;
- Valores negociados;
- Obrigações de cada uma das partes;
- Vigência do contrato;
- Cláusulas de rescisão;
"""

tags_metadata = [
    {"name": "login", "description": "Interface para login na aplicação."},
    {"name": "contracts", "description": "Operações de envio e retorno de contratos."},
]

app = FastAPI(
    title="Analisador de Contratos com IA | Biofy",
    description=application_description,
    summary="Analisador de Contratos com IA Generativa.",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
)

origins = ["*"]  # For development.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(contracts_router)


@app.post("/login", response_model=Token, tags=["login"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    token = create_access_token(data={"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

# This route serves your index.html file as the main page
@app.get("/", response_class=FileResponse, include_in_schema=False)
async def read_index():
    return FileResponse("static/index.html")

# Mounts the 'static' directory.
# FastAPI will look for files in the 'static' folder if no other API route matches.
app.mount("/static", StaticFiles(directory="static"), name="static")