# This is the file defining the Ronde class
from datetime import datetime


class Round:
    def __init__(self, name, games, tournament_name):
        self.name = name
        self.games = games
        self.tournament_name = tournament_name
        self.starting_date = datetime.now().strftime('%d-%m-%Y')
        self.starting_hour = datetime.now().strftime('%H:%M:%S')

    def add_tournament(self, tournament):
        serialized_round = {
            'name': self.name,
            'starting_date': self.starting_date,
            'starting_hour': self.starting_hour,
            'ending_date': datetime.now().strftime('%d-%m-%Y'),
            'ending_hour': datetime.now().strftime('%H:%M:%S'),
            'games': self.games
        }
        tournament.rounds.append(serialized_round)
        return
