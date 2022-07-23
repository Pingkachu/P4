# This is the file defining the Match class
from tinydb import TinyDB


class Game:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def add_db(self):
        db = TinyDB('db.json')
        games_table = db.table('games')
        serialized_game = {
            'joueur1': self.p1['name'],
            'joueur2': self.p2['name'],
            'score_j1': self.p1['points'],
            'score_j2': self.p2['points'],
        }

        # Ajout Tournoi dans la base

        games_table.insert(serialized_game)
