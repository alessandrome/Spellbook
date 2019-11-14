from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class CharacterClassSpellPivot(Base):
    __tablename__ = 'classeincantesimi'
    NomeIncantesimo = Column(String(100), ForeignKey('incantesimi.Nome'), primary_key=True)
    NomeClasse = Column(String(45), ForeignKey('classe.Nome'), primary_key=True)
    Classe = relationship("CharacterClass")


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
    Classi = relationship('CharacterClassSpellPivot')


class CharacterClass(Base):
    __tablename__ = 'classe'
    Nome = Column(String, primary_key=True)
