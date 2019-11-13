from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database.base import Base
from database.characterclass_spell_pivot import CharacterClassSpellPivot


class Spell(Base):
    __tablename__ = 'incantesimi'
    Nome = Column(String(100), primary_key=True)
    Tipo = Column(String(45))
    Livello = Column(Integer)
    TempoDiLancio = Column(String(255))
    Gittata = Column(String(100))
    Componenti = Column(String(512))
    Durata = Column(String(45))
    Descrizione = Column(Text)
    # Classe = relationship("CharacterClass",
    #                         secondary=CharacterClassSpellPivot.__table__,
    #                         backref="classe")
