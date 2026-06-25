from database.DB_connect import DBConnect
from model.Actor import Actor


class DAO:
    def __init__(self):
        raise NotImplementedError("Non istanziare il DAO")

    @staticmethod
    def get_all_actors_in_rating_range(min_rating: float, max_rating: float) -> list[Actor]:
        """
        Restituisce tutti gli attori che hanno recitato in film con rating medio che sta nel range
        """
        query = """
        SELECT DISTINCT(N.id), N.name, N.date_of_birth FROM role_mapping RM, movie MV, names N, ratings RT
	    WHERE RM.movie_id = MV.id AND
	    N.id = RM.name_id AND
            N.date_of_birth IS NOT NULL AND
	    RT.movie_id = MV.id AND 
	    RT.avg_rating >= %s AND RT.avg_rating <= %s
	;
        """

        data = tuple([min_rating, max_rating])
        connection = DBConnect.get_connection()
        cursor = connection.cursor(dictionary = True)
        cursor.execute(query, data)

        res = []
        for row in cursor:
            res.append(Actor(
                id=row["id"],
                name=row["name"],
                date_of_birth=row["date_of_birth"]
            ))

        cursor.close()
        connection.close()
        return res

    @staticmethod
    def get_statistics_table(min_rating, max_rating):
        query = """
        SELECT MV.id as movie_id, N.id as actor_id, MV.worlwide_gross_income 
        FROM role_mapping RM, movie MV, names N, ratings RT
            WHERE RM.movie_id = MV.id AND
            N.id = RM.name_id AND
            RT.movie_id = MV.id AND 
            MV.worlwide_gross_income IS NOT NULL AND
            N.date_of_birth IS NOT NULL AND
            RT.avg_rating >= %s AND RT.avg_rating <= %s
        ;
        """

        data = tuple([min_rating, max_rating])
        connection = DBConnect.get_connection()
        cursor = connection.cursor(dictionary = True)
        cursor.execute(query, data)

        res =  cursor.fetchall()
        cursor.close()
        connection.close()
        return res