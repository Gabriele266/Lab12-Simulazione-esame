import itertools
from collections import defaultdict

import networkx as nx

from database.DAO import DAO
from model.Actor import Actor


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self._id_map: defaultdict[str, Actor] = defaultdict()

    def create_graph(self):
        actors = DAO.get_all_actors_in_rating_range(1.2, 2.7)

        # Creo la id map
        self._id_map = defaultdict()
        for actor in actors:
            self._id_map[actor.id] = actor

        self.graph.add_nodes_from(actors)

        statistic_table = DAO.get_statistics_table(1.2, 2.7)

        for a, b in itertools.combinations(actors, 2):
            # Film in cui ha recitato l'attore A, sotto forma di id-map a partire dalla tabella statistiche
            films_a = self.load_films_for_actor(a.id, statistic_table)

            # Film in cui ha recitato l'attore B
            films_b = self.load_films_for_actor(b.id, statistic_table)

            intersection = set(films_a.keys()) & set(films_b.keys())
            if len(intersection) > 0:    # I due attori hanno almeno un film in comune
                movies_in_common = { k: films_a[k] for k in intersection}       # Informazioni sui film in comune prese dalla tabella delle statistiche
                weight = self.__calc_weight(movies_in_common)
                self.graph.add_edge(a, b, weight=weight)


    def load_films_for_actor(self, id: str, all_actors_stat):
        id_map = defaultdict()

        for a_row in all_actors_stat:
            if a_row["actor_id"] == id:
                id_map[a_row["movie_id"]] = a_row["worlwide_gross_income"]

        return id_map

    def __calc_weight(self, movies_in_common):
        s = 0
        for r in movies_in_common.keys():
            str_value = movies_in_common[r]
            if str_value is not None:
                s += int(str_value.replace("$", ""))
        return s