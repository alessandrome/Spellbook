from sqlalchemy import Column, String
from database.base import Base


class CharacterClass(Base):
    __tablename__ = 'classe'
    Nome = Column(String, primary_key=True)
