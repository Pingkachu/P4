# This is the file defining the Tournmament class
from tinydb import TinyDB
from tinydb import Query
from datetime import datetime


class Tournament:

    def __init__(self, name, location, time, description, players):
        self.name = name
        self.location = location
        self.date = datetime.now().strftime('%d-%m-%Y')
        self.nb_rounds = 4
        self.rounds = []
        self.players = players
        self.time = time
        self.description = description

    def add_tournament(self):
        db = TinyDB('db.json')
        serialized_tournament = {
            'name': self.name,
            'location': self.location,
            'date': self.date,
            'players': self.players,
            'time': self.time,
            'description': self.description,
            'rounds': self.rounds,
            'nb_rounds': self.nb_rounds
        }

        # Ajout Tournoi dans la base
        tournaments_table = db.table('tournaments')
        tournaments_table.insert(serialized_tournament)

    def update_rounds(self):
        db = TinyDB('db.json')
        to_table = db.table('tournaments')
        to_table.update({'rounds': self.rounds}, Query()['name'] == self.name)
