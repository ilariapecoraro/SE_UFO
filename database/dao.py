from database.DB_connect import DBConnect
from model.state import State

class DAO:

    @staticmethod
    # metodo che estrae tutte le forme disponibili
    @staticmethod
    def get_all_states():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM state """

        cursor.execute(query)

        for row in cursor:
            result.append(State(row["id"], row["name"], row["capital"],
                                row["lat"], row["lng"], row["area"],
                                row["population"], row["neighbors"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connection(year, shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
        SELECT LEAST(n.state1, n.state2) AS st1,
        GREATEST(n.state1, n.state2) AS st2, 
        COUNT(*) as peso
        FROM sighting s , neighbor n 
        WHERE year(s.s_datetime) = %s
        AND s.shape = %s
        AND (s.state = n.state1 OR s.state = n.state2)
        GROUP BY st1 , st2

         """

        cursor.execute(query,(year,shape))

        for row in cursor:
            result.append((row["st1"],row["st2"],row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    # metodo che estrae tutti gli anni disponibili
    def get_all_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
         SELECT DISTINCT YEAR(s_datetime) AS anno
         FROM sighting
         WHERE YEAR(s_datetime ) >= 1910 AND YEAR(s_datetime ) <2015
         """

        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    # metodo che estrae tutte le forme disponibili
    def get_all_shapes(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
             SELECT DISTINCT shape
            FROM sighting
            WHERE YEAR(s_datetime ) = %s
             """

        cursor.execute(query,(year,))

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result