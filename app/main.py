from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .auth import authenticate_user, create_access_token
from .schemas import Token
from .contracts import router as contracts_router
from .database import Base, engine
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Analisador de Contratos com IA | Biofy",
    description="""
Esta aplicação facilita a análise de contratos jurídicos utilizando o auxílio de inteligência artificial generativa.

Por meio desta interface o usuário pode fazer o upload de documentos nos formatos .pdf e .docx para serem analisados.

São retornados detalhes críticos dos contratos como:
- As partes envolvidas;
- Valores negociados;
- Obrigações de cada uma das partes;
- Vigência do contrato;
- Cláusulas de rescisão;
""",
    summary="Analisador de Contratos com IA Generativa.",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.include_router(contracts_router)


@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    token = create_access_token(data={"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}
