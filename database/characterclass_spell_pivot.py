from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from database import CharacterClass


class CharacterClassSpellPivot(Base):
    __tablename__ = 'classeincantesimi'
    NomeIncantesimo = Column(String(100), ForeignKey('incantesimi.Nome'), primary_key=True)
    NomeClasse = Column(String(45), ForeignKey('classe.Nome'), primary_key=True)
    # Classe = relationship(CharacterClass.__name__, back_populates="classe")
