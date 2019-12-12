from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class Spell(Base):
    __tablename__ = 'spells'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), index=True)
    type = Column(String(45))
    level = Column(Integer)
    casting_time = Column(String(255))
    range = Column(String(100))
    components = Column(String(512))
    duration = Column(String(45))
    description = Column(Text)
    classes = relationship('CharacterClass', secondary='class_spell', backref='spells')


class CharacterClass(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    name = Column(String(45), index=True)


class CharacterClassSpellPivot(Base):
    __tablename__ = 'class_spell'
    spell_id = Column(Integer, ForeignKey('spells.id'), primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'), primary_key=True)
    character_class = relationship("CharacterClass")
    spell = relationship("Spell")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)


class Favourite(Base):
    __tablename__ = 'favourites'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    spell_id = Column(Integer, ForeignKey('spells.id'), primary_key=True)
    user = relationship('User')
    spell = relationship('Spell')
