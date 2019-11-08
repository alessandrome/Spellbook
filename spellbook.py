import pymysql
pymysql.install_as_MySQLdb()  # This must be init here before import MySQLdb
import MySQLdb


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

    def ottieniIncantesimiDiLivello(self,lvl):
        query = ("CALL `ottieniIncantesimiDiLivello`('"+str(lvl)+"');")
        self.cursor.execute(query)
        contentList = []
        aux = {}
        for row in self.cursor:
            aux["Classe"] = row[8]
            aux["Nome"] = row[0]
            aux["Tipo"] = row[1]
            aux["Livello"] = row[2]
            aux["TempoDiLancio"] = row[3]
            aux["Componenti"] = row[4]
            aux["Durata"] = row[5]
            aux["Gittata"] = row[6]
            aux["Descrizione"] = row[7]
            
            contentList.append(aux)
            aux = {}
        return contentList
    def ottieniIncantesimiPerClasseDiLivello(self,classe,lvl):
        query = ("CALL `ottieniIncantesimiPerClasseDiLivello`('"+classe+"','"+str(lvl)+"');")
        self.cursor.execute(query)
        contentList = []
        aux = {}
        for row in self.cursor:
            aux["Classe"] = row[8]
            aux["Nome"] = row[0]
            aux["Tipo"] = row[1]
            aux["Livello"] = row[2]
            aux["TempoDiLancio"] = row[3]
            aux["Componenti"] = row[4]
            aux["Durata"] = row[5]
            aux["Gittata"] = row[6]
            aux["Descrizione"] = row[7]
            
            contentList.append(aux)
            aux = {}
        return contentList
    def ottieniIncantesimiPerClasse(self,classe):
        query = ("CALL `ottieniIncantesimiPerClasse`('"+classe+"');")
        self.cursor.execute(query)
        contentList = []
        aux = {}
        for row in self.cursor:
            aux["Classe"] = row[8]
            aux["Nome"] = row[0]
            aux["Tipo"] = row[1]
            aux["Livello"] = row[2]
            aux["TempoDiLancio"] = row[3]
            aux["Componenti"] = row[4]
            aux["Durata"] = row[5]
            aux["Gittata"] = row[6]
            aux["Descrizione"] = row[7]
            
            contentList.append(aux)
            aux = {}
        return contentList
    def ottieniIncantesimiPerNome(self,nome):
        query = ("CALL `ottieniIncantesimiPerNome`('"+nome+"');")
        self.cursor.execute(query)
        contentList = []
        aux = {}
        for row in self.cursor:
            aux["Classe"] = row[8]
            aux["Nome"] = row[0]
            aux["Tipo"] = row[1]
            aux["Livello"] = row[2]
            aux["TempoDiLancio"] = row[3]
            aux["Componenti"] = row[4]
            aux["Durata"] = row[5]
            aux["Gittata"] = row[6]
            aux["Descrizione"] = row[7]
            
            contentList.append(aux)
            aux = {}
        return contentList
    def aggiungiUtente(self,userId):
        try:
            query = ("CALL `aggiungiUtente`('"+str(userId)+"');")
            self.cursor.execute(query)
            self.cn_object.commit()
            return True
        except:
            return False
    def aggiungiPreferiti(self,userId,incantesimo):
        try:
            query = ("CALL `aggiungiPreferiti`('"+str(userId)+"','"+incantesimo+"');")
            self.cursor.execute(query)
            self.cn_object.commit()
            return True;
        except:
            return False
    def rimuoviPreferiti(self,userId,incantesimo):
        try:
            query = ("CALL `rimuoviPreferiti`('"+str(userId)+"','"+incantesimo+"');")
            self.cursor.execute(query)
            self.cn_object.commit()
            return True;
        except:
            return False
    def ottieniPreferiti(self, idUser):
        query = ("CALL `ottieniPreferiti`('"+str(idUser)+"');")
        self.cursor.execute(query)
        contentList = []
        aux = {}
        for row in self.cursor:
            aux["Classe"] = row[8]
            aux["Nome"] = row[0]
            aux["Tipo"] = row[1]
            aux["Livello"] = row[2]
            aux["TempoDiLancio"] = row[3]
            aux["Componenti"] = row[4]
            aux["Durata"] = row[5]
            aux["Gittata"] = row[6]
            aux["Descrizione"] = row[7]
            
            contentList.append(aux)
            aux = {}
        return contentList
    def stampaRisultato(self,content):
        for tupla in content:
            for nomeColonna, valore in tupla.items():
                print(nomeColonna+" : "+str(valore))
        
        
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
