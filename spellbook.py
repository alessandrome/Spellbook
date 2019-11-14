import pymysql
pymysql.install_as_MySQLdb()  # This must be init here before import MySQLdb
import MySQLdb
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import database


class Spellbook:
    def __init__(self, user_name, user_pwd, url='127.0.0.1', db_name='spellbook', db_port=3306):
        if url is None:
            url = '127.0.0.1'
        if db_name is None:
            db_name = 'spellbook'
        if db_port is None:
            db_port = 3306
        self.url = url
        self.user_name = user_name
        self.user_pwd = user_pwd
        self.db_name = db_name
        self.db_port = db_port
        # TODO: Add Exception for wrong DB connection
        # Connect to DB
        self.cn_object = None
        self.cursor = None
        self.engine = create_engine(
            'mysql://{}:{}@{}:{}/{}'.format(self.user_name, self.user_pwd, self.url, self.db_port, self.db_name))
        self.engine_connection = self.engine.connect()
        self.EngineSession = sessionmaker(bind=self.engine)
        # TODO: With SQLAlchemy this will not be more needed
        self.cn_object = MySQLdb.connect(
            self.url,
            self.user_name,
            self.user_pwd,
            self.db_name,
            self.db_port
        )
        self.cursor = self.cn_object.cursor()

    def __del__(self):
        if self.cn_object:
            self.cn_object.close()
        if self.cursor:
            self.cursor.close()

    def get_classes(self):
        session = self.EngineSession()
        return session.query(database.CharacterClass).all()

    def get_spells_by_level(self, lvl):
        session = self.EngineSession()
        return session.query(database.Spell).filter_by(Livello=lvl).order_by(sqlalchemy.asc(database.Spell.Nome)).all()

    def get_spells_by_level_class(self, character_class, lvl):
        session = self.EngineSession()
        return session.query(database.Spell)\
            .filter(database.Spell.Livello==lvl)\
            .filter(database.CharacterClass.Nome==character_class)\
            .order_by(sqlalchemy.asc(database.Spell.Nome))\
            .all()

    def get_spells_by_class(self, character_class):
        query = ("CALL `ottieniIncantesimiPerClasse`('{}');".format(character_class))
        result = self.engine_connection.execute(query)
        content_list = []
        for row in result:
            content_list.append({
                "Classe": row[8],
                "Nome": row[0],
                "Tipo": row[1],
                "Livello": row[2],
                "TempoDiLancio": row[3],
                "Componenti": row[4],
                "Durata": row[5],
                "Gittata": row[6],
                "Descrizione": row[7],
            })

        return content_list

    def get_spells_by_name(self, name):
        query = ("CALL `ottieniIncantesimiPerNome`('{}');".format(name))
        self.cursor.execute(query)
        content_list = []
        for row in self.cursor:
            content_list.append({
                "Classe": row[8],
                "Nome": row[0],
                "Tipo": row[1],
                "Livello": row[2],
                "TempoDiLancio": row[3],
                "Componenti": row[4],
                "Durata": row[5],
                "Gittata": row[6],
                "Descrizione": row[7],
            })
        return content_list

    # TODO: RE-factory from here
    def add_user(self, user_id):
        try:
            query = ("CALL `aggiungiUtente`('{}');".format(str(user_id)))
            self.engine_connection.execute(query)
            # self.cn_object.commit()
            return True
        except:
            return False

    def add_favourite(self, user_id, spell):
        try:
            query = ("CALL `aggiungiPreferiti`('{}','{}');".format(str(user_id), spell))
            self.engine_connection.execute(query)
            # self.cn_object.commit()
            return True
        except:
            return False

    def remove_favourite(self, user_id, spell):
        try:
            query = ("CALL `rimuoviPreferiti`('{}','{}');".format(user_id, spell))
            self.engine_connection.execute(query)
            # self.cn_object.commit()
            return True
        except:
            return False

    def get_favourites(self, user_id):
        query = ("CALL `ottieniPreferiti`('{}');".format(user_id))
        self.engine_connection.execute(query)
        content_list = []
        for row in self.cursor:
            content_list.append({
                "Classe": row[8],
                "Nome": row[0],
                "Tipo": row[1],
                "Livello": row[2],
                "TempoDiLancio": row[3],
                "Componenti": row[4],
                "Durata": row[5],
                "Gittata": row[6],
                "Descrizione": row[7],
            })
        return content_list

    def print_result(self, content):
        for row in content:
            for column_name, value in row.items():
                print('{}: {}'.format(column_name, value))


'''
obj = Spellbook("standard","guruguru","localhost","dnd_5_incantesimi")

obj.stampaRisultato(obj.ottieniIncantesimiDiLivello(2))
obj.stampaRisultato(obj.ottieniIncantesimiPerNome("Ami"))

print(obj.aggiungiUtente(123456))
print(obj.aggiungiPreferiti(123456,"Amicizia"))
print(obj.rimuoviPreferiti(123456,"Amicizia"))
print(obj.aggiungiPreferiti(123456,"Amicizia"))
obj.stampaRisultato(obj.ottieniPreferiti(123456))
'''
