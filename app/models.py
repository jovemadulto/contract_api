from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    contratante = Column(Text)
    contratado = Column(Text)
    valor_bens = Column(Text)
    obrigacoes_contratante = Column(Text)
    obrigacoes_contratada = Column(Text)
    objeto = Column(Text)
    vigencia = Column(Text)
    clausula_rescisao = Column(Text)
