from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from .auth import get_current_user
from .models import Contract
from .schemas import ContractData
from .ai_service import extract_contract_info
import os
from docx import Document
import pymupdf

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def extract_text_from_file(file: UploadFile):
    if file.filename.endswith(".pdf"):
        reader = pymupdf.open(file.filename)
        pdf_content = []

        for page in reader.pages():
            for block in page.get_text(option="blocks"):
                _, _, _, _, content, _, block_type = block
                if block_type == 0:
                    # https://pymupdf.readthedocs.io/en/latest/textpage.html#TextPage.extractBLOCKS
                    #
                    # Blocks do tipo 0 são aqueles identificados como sendo de texto puro
                    # Desta forma eliminamos a necessidade de consumir blocos de imagens
                    # -- e a possibilidade de passar metadados delas -- como conteúdo
                    # de texto para o modelo avaliar
                    #
                    # A abordagem de iterar sobre os blocos também pode se mostrar útil para facilitar o
                    # descarte de pedaços do documento, como páginas e metadados de rodapé e de assinatura digital
                    #
                    # Essas decisões de projeto devem resultar em um consumo menor de tokens e
                    # aumentar a qualidade da resposta

                    pdf_content.append(content.strip())

        ## TO-DO : Implementar solução de OCR

        # Criar funções separadas para processar contratos em PDF:
        # 1. Firmados em texto puro ✔
        # 2. Escaneados
        # 2.1 O PyMuPDF tem suporte de compatibilidade com o PyTesseract
        #     https://pymupdf.readthedocs.io/en/latest/installation.html#installation-ocr

        return "\n".join(pdf_content)
    elif file.filename.endswith(".docx"):
        doc = Document(file.file)

        return "\n".join([p.text for p in doc.paragraphs])
    else:
        raise HTTPException(
            status_code=400,
            detail="Formato de arquivo inválido. Somente arquivos .pdf e .docx são aceitos.",
        )


@router.post(
    "/contracts/upload",
    response_model=ContractData,
    tags=["contracts"],
    summary="Envio de contratos para análise",
    description="""
Aceita documentos em formato *.pdf e *.docx.\n
Envia o conteúdo de texto desses arquivos para a infraestrutura da Google para ser analisado pela Gemini.\n
Atualmente só aceita o modelo `gemini-2.5-flash-lite`\n
Retorna dados considerados críticos em uma análise de contratos, como:
- Nome da parte contratante
- Nome da parte contratada
- Valor dos bens negociados
- Obrigações da parte contratante
- Obrigações da parte contratada
- Objeto negociado
- Vigência do contrato
- Cláusulas de rescisão previstas
""",
)
def upload_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    text = extract_text_from_file(file)
    info = extract_contract_info(text)

    contract = Contract(filename=file.filename, **info)
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


@router.get(
    "/contracts/{filename}",
    response_model=ContractData,
    tags=["contracts"],
    summary="Recuperação de dados analisados",
    description="""
Recupera os dados de contratos submetidos para análise pelo serviço de inteligência artificial.
""",
)
def get_contract(
    filename: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    # Para fins de teste de aplicação, a verificação através do nome e UUID é suficiente
    # para recuperar o contrato correto.
    #
    # É necessário, porém, criar validação também para que o usuário possa recuperar
    # somente os contratos enviados por ele próprio, por questões de privacidade e negócio

    contract = db.query(Contract).filter(Contract.filename == filename).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")
    return contract
