from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting

class DAO:
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
    def get_all_sighting():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * 
                    FROM sighting
                    ORDER BY s_datetime ASC """

        cursor.execute(query)

        for row in cursor:
            result.append(Sighting(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_shapes(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT shape 
                    FROM sighting 
                    WHERE shape <> "" AND YEAR(s_datetime) = %s """

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(row['shape'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_weighted_neigh(year, shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT LEAST(n.state1, n.state2) AS st1,
                           GREATEST(n.state1, n.state2) AS st2, 
                           COUNT(*) as N
                    FROM sighting s , neighbor n 
                    WHERE year(s.s_datetime) = %s
                          AND s.shape = %s
                          AND (s.state = n.state1 OR s.state = n.state2)
                    GROUP BY st1 , st2 """

        cursor.execute(query, (year, shape))

        for row in cursor:
            result.append((row['st1'], row['st2'], row["N"]))

        cursor.close()
        conn.close()
        return result