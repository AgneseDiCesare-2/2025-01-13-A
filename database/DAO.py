from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                           FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_classifications():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM classification"""
            cursor.execute(query)

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getLocalization():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct c.Localization as l
                        from classification c 
                        order by c.Localization DESC """
            cursor.execute(query)

            for row in cursor:
                result.append(row["l"]) #lista di stringhe

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodi(localization):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct c.*, g.Essential 
                        from classification c, genes g 
                        where c.GeneID =g.GeneID  and c.Localization=%s"""
            cursor.execute(query, (localization, ))

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getArchi():
        #controlla in Python se sono tra i nodi
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct i.GeneID1, i.GeneID2, sum(distinct g.Chromosome ) as peso
                        from interactions i, genes g 
                        where (g.GeneID =i.GeneID1 or g.GeneID = i.GeneID2)
                        and i.GeneID1 <> i.GeneID2
                        group by i.GeneID1, i.GeneID2"""
            cursor.execute(query)

            for row in cursor:
                result.append((row["GeneID1"], row["GeneID2"], row["peso"]))

            cursor.close()
            cnx.close()
        return result
