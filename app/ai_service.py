from dotenv import load_dotenv
import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel
from pprint import pprint

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class ModelAnswer(BaseModel):
    """
    Como requisito de processamento de contrato, são consideradas informações essenciais:
    - Nome das partes
    - Valores monetários
    - Obrigações principais
    - Dados adicionais importantes (objeto, vigência)
    - Cláusula de Rescisão
    """

    contratante: list[str]
    contratado: list[str]
    valor_bens: str
    obrigacoes_contratante: list[str]
    obrigacoes_contratada: list[str]
    objeto: list[str]
    vigencia: str
    clausula_rescisao: str


def extract_contract_info(contract_content: str) -> dict:
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=contract_content,
        config={
            "response_mime_type": "application/json",
            "response_schema": list[ModelAnswer],
            "system_instruction": """
            Você está recebendo um contrato.
            Sua tarefa é identificar dados importantes neste documento.
            São considerados dados importantes:
            1. Nome da parte contratante;
            2. Nome da parte contratada;
            3. Valor dos bens;
            4. As obrigações que devem ser cumpridas pela parte contratante;
            6. As obrigações que devem ser cumpridas pela parte contratada;
            7. A descrição do objeto do contrato;
            8. A vigência do contrato;
            9. A descrição da(s) cláusula(s) de rescisão;
            """,
        },
    )

    response = response.model_dump().get("parsed")[0]  # -> dict

    for field in [
        "contratante",
        "contratado",
        "objeto",
        "obrigacoes_contratante",
        "obrigacoes_contratada",
    ]:
        response[field] = json.dumps(response[field])

    pprint(response)

    return response
