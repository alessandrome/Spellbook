from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class CharacterClassSpellPivot(Base):
    __tablename__ = 'classeincantesimo'
    NomeIncantesimo = Column(String(100), ForeignKey('incantesimi.Nome'), primary_key=True)
    NomeClasse = Column(String(45), ForeignKey('classe.Nome'), primary_key=True)
    Classe = relationship("CharacterClass")
    Incantesimo = relationship("Spell")


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
    Classi = relationship('CharacterClass', secondary='classeincantesimo', backref='Incantesimi')


class CharacterClass(Base):
    __tablename__ = 'classe'
    Nome = Column(String, primary_key=True)


class User(Base):
    __tablename__ = 'user'
    IdUser = Column(Integer, primary_key=True)


class Favourite(Base):
    __tablename__ = 'preferiti'
    IdUser = Column(Integer, ForeignKey('user.IdUser'), primary_key=True)
    NomeIncantesimo = Column(String(100), ForeignKey('incantesimi.Nome'), primary_key=True)
    User = relationship('User')
    Incantesimo = relationship('Spell')
