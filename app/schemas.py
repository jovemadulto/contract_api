from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    username: str
    password: str


class ContractData(BaseModel):
    # O valor dos bens é um dado particularmente delicado em razão da sua natureza.
    #
    # É possível armazenar definir esta coluna no banco de dados como INTEGER
    # (com valores devidamente convertidos para centavos)
    # mas para tanto seria necessário ter certeza de que o processamento
    # do LLM retorna valores coesos.
    #
    # Há possibilidade de manter o valor como STRING e garantir que a conversão
    # obedeça regras mais explícitas via aplicação, e não ocorra no banco de dados.

    id: int
    filename: str
    contratante: str
    contratado: str
    valor_bens: str
    obrigacoes_contratante: str
    obrigacoes_contratada: str
    objeto: str
    vigencia: str
    clausula_rescisao: str

