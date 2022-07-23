# This is the file defining the Joueur class
from tinydb import TinyDB

db = TinyDB('db.json')
players_table = db.table('players')


class Player:
    def __init__(self, surname, name, elo, gender, birthdate):
        self.name = name
        self.surname = surname
        self.elo = elo
        self.gender = gender
        self.birthdate = birthdate

    # def ajout_point(self):

    def add_player(self):
        serialized_player = {
            'name': self.name,
            'surname': self.surname,
            'elo': self.elo,
            'gender': self.gender,
            'birthdate': self.birthdate
        }

        # Ajout Joueur dans la base
        players_table.insert(serialized_player)
        return
