# This is a sample Python script.

from PlayerHandle import Player
from GameHandle import Game
from RoundHandle import Round
from TournamentHandle import Tournament
from tinydb import TinyDB
from tinydb import Query

db = TinyDB('db.json')
tournaments_table = db.table('tournaments')
players_table = db.table('players')

# global variable to store players points and name
players_points = {}

main_menu_options = {
    1: 'Ajouter un joueur',
    2: 'Créer un tournoi',
    3: 'Afficher des informations en rapport avec un tournoi',
    4: 'Modifier le classement d\'un joueur',
    5: 'Quitter',
}

second_menu_options = {
    1: 'Liste de tous les acteurs (ordre aphabétique)',
    2: 'Liste de tous les acteurs (par classement)',
    3: 'Liste de tous les joueurs d\'un tournoi (ordre alphabétique)',
    4: 'Liste de tous les joueurs d\'un tournoi (par classement)',
    5: 'Liste de tous les tournois',
    6: 'Liste de toutes les rondes d\'un tournoi',
    7: 'Liste de tous les matchs d\'un tournoi',
    8: 'Retour au menu principal',
}


def start_tournament(tournament):

    pl_searched = []
    reload_db = TinyDB('db.json')
    reload_ptable = reload_db.table('players')

    # Search and save each players elo and points
    for k in range(8):
        name_pl = tournament.players[k]
        pl_searched.append(reload_ptable.search(Query()['name'] == name_pl)[0])
        info_pl = {"elo": pl_searched[k]['elo'], "points": 0, "fought": []}
        players_points[name_pl] = info_pl

    # Creating games for the first round, based on players' elo
    pl_searched.sort(key=lambda x: x['elo'])
    games_r1 = []
    for k in range(4):
        name_p1 = pl_searched[k]['name']
        name_p2 = pl_searched[k+4]['name']
        p1 = {'name': name_p1, 'points': 0}
        p2 = {'name': name_p2, 'points': 0}
        games_r1.append([p1, p2])
        players_points[name_p1]['fought'].append(name_p2)
        players_points[name_p2]['fought'].append(name_p1)
    round1 = Round('Ronde 1', games_r1, tournament.name)
    return round1


def display_games_to_play(swiss_round):
    names_p1 = []
    names_p2 = []
    for game in swiss_round.games:
        names_p1.append(game[0]['name'])
        names_p2.append(game[1]['name'])

    games_list = {
        "#": 'Voici les matchs à jouer : ',
        "Match 1": names_p1[0] + " VS " + names_p2[0],
        "Match 2": names_p1[1] + " VS " + names_p2[1],
        "Match 3": names_p1[2] + " VS " + names_p2[2],
        "Match 4": names_p1[3] + " VS " + names_p2[3],
    }
    print_menu(games_list)


def enter_round_result(swiss_round, tournament):
    print("Entrez 1 pour une victoire, 0 pour une défaite et 0.5 pour un nul")
    # For each game
    for game in swiss_round.games:
        # Update the result for each player of the game, then save it
        for pl in game:
            successful = False
            while not successful:
                try:
                    pl['points'] = float(input("Entrez le résultat "
                                               "de " + pl['name'] + "\n"))
                    successful = True
                except ValueError:
                    print("Mauvaise option. Introduiser un chiffre...\n")
            points_to_add = players_points[pl['name']]["points"] + pl['points']
            players_points[pl['name']]["points"] = points_to_add
        Game(game[0], game[1]).add_db()
    swiss_round.add_tournament(tournament)
    return


def start_next_round(number_round, tournament_name):
    # Sorting players based on points, then elo
    list_player = players_points.items()
    sorted_players = sorted(list_player,
                            key=lambda x: (x[1]["points"], x[1]["elo"]))
    # Creation of the games for the next round
    games = []
    for k in range(0, 8, 2):
        # Check if players fought each other in previous rounds
        for items in players_points[sorted_players[k+1][0]]["fought"]:
            if items == sorted_players[k][0]:
                temp_player = sorted_players[k]
                temp_player_1 = sorted_players[k+1]
                sorted_players[k+1] = temp_player
                sorted_players[k] = temp_player_1
        p1 = sorted_players[k][0]
        p2 = sorted_players[k+1][0]
        games.append([{'name': p1, 'points': 0}, {'name': p2, 'points': 0}])
        players_points[p1]['fought'].append(p2[0])
        players_points[p2]['fought'].append(p1)
    return Round('Ronde ' + str(number_round), games, tournament_name)


def display_tournament_result():
    tournament_result = {}
    for name_p in players_points:
        tournament_result[name_p] = players_points[name_p]['points']
    print_menu(tournament_result)
    for name_p in players_points:
        print("Modifier le classement de : " + name_p)
        modify_elo_player(name_p)
    print("")
    return


def modify_elo_player(name_p):
    try:
        elo = int(input('Rentrez le nouveau classement : '))
    except ValueError:
        print("Mauvaise option. Introduiser un chiffre...\n")
        return
    players_table.update({'elo': elo}, Query().name == name_p)
    return


def enter_player_info():
    name = input("Entrez le nom : ")
    surname = input("Entrez le prénom : ")
    try:
        elo = int(input("Entrez le classement : "))
    except ValueError:
        print("Erreur, veuillez introduire un chiffre...")
        return
    gender = input("Entrez le genre de la personne (M ou F) : ")
    birthdate = input("Entrez la date de naissance (dd/mm/yyyy) : ")

    p = Player(surname, name, elo, gender, birthdate)
    # Envoi les infos pour l'ajout en base de données
    p.add_player()
    return name


def enter_tournament_info():

    name_t = input("Entrez le nom : ")
    location = input("Entrez le lieu : ")
    time = input("Quel temps utilisé ? Blitz/Bullet/Coup rapide : ")
    description = input("Entrez la descritpion du tournoi : ")
    players = []
    print("Entrez le noms des joueurs du tournoi")
    for k in range(8):
        print("Joueur " + str(k+1))
        name_p = input()
        exist = players_table.search(Query()['name'] == name_p)
        # Query sur vérification du joueur en base
        if not exist:
            print("Veuillez ajouter ce joueur dans la base de données \n")
            name_p = enter_player_info()
        players.append(name_p)

    tournament = Tournament(name_t, location, time, description, players)
    tournament.add_tournament()

    return tournament


def get_all_players(sorting):
    serialized_players = players_table.all()
    serialized_players.sort(key=lambda x: x[sorting])
    for item in serialized_players:
        print(item['name']+" "+str(item['elo']))
    return


def get_all_tournament_players(to_name, sorting):

    to_searched = tournaments_table.search(Query()['name'] == to_name)[0]
    pls_searched = []
    for item in to_searched['players']:
        pls_searched.append(players_table.search(Query()['name'] == item)[0])
    pls_searched.sort(key=lambda x: x[sorting])

    for player in pls_searched:
        print(player['name']+" "+str(player['elo']))
    return


def get_all_tournaments():
    # Display all tournaments names
    serialized_tournaments = tournaments_table.all()
    for tournament in serialized_tournaments:
        print(tournament['name'])
    return


# A corriger
def get_all_tournament_rounds(to_name):
    # A finir
    to_searched = tournaments_table.search(Query()['name'] == to_name)[0]
    for swiss_round in to_searched['rounds']:
        print(swiss_round)


# A corriger
def get_all_tournament_games(to_name):
    # A finir
    to_searched = tournaments_table.search(Query()['name'] == to_name)[0]
    for swiss_round in to_searched['rounds']:
        for game in swiss_round['games']:
            print(str(game[0])+" VS "+str(game[1]))


def display_second_menu():
    print_menu(second_menu_options)
    select = ''
    try:
        select = int(input("Entrer votre choix : "))
    except ValueError:
        print("Mauvaise option. Introduiser un chiffre...")
    if select == 1:
        get_all_players('name')
        # Arrêt de la capture du clavier

    elif select == 2:
        get_all_players('elo')

    elif select == 3:
        tournament_name = input("Quelle tournoi cherchez-vous ? ")
        get_all_tournament_players(tournament_name, 'name')

    elif select == 4:
        tournament_name = input("Quelle tournoi cherchez-vous ? ")
        get_all_tournament_players(tournament_name, 'elo')

    elif select == 5:
        get_all_tournaments()

    elif select == 6:
        tournament_name = input("Quelle tournoi cherchez-vous ? ")
        get_all_tournament_rounds(tournament_name)

    elif select == 7:
        tournament_name = input("Quelle tournoi cherchez-vous ? ")
        get_all_tournament_games(tournament_name)

    elif select == 8:
        return
    else:
        print('Mauvais choix. Entrer un nombre entre 1 et 8')


def print_menu(menu_options):
    for key in menu_options.keys():
        print(key, ')', menu_options[key])
    return


if __name__ == '__main__':
    # Choix Menu
    print("Pour sélectionner un élément du menu, "
          "taper le numéro correspondant. \n")
    while True:
        print_menu(main_menu_options)
        choice = ''
        try:
            choice = int(input('Entrer votre choix: \n'))
        except ValueError:
            print('Mauvaise option. Introduiser un chiffre...\n')
            continue

        if choice == 1:
            enter_player_info()
            # Arrêt de la capture du clavier

        elif choice == 2:
            newTournament = enter_tournament_info()
            first_round = start_tournament(newTournament)
            display_games_to_play(first_round)
            enter_round_result(first_round, newTournament)
            for i in range(2, 5, 1):
                new_round = start_next_round(i, newTournament.name)
                display_games_to_play(new_round)
                enter_round_result(new_round, newTournament)
            newTournament.update_rounds()
            display_tournament_result()

        elif choice == 3:
            display_second_menu()
            option = ""

        elif choice == 4:
            player_name = input("Rentrez le nom du joueur "
                                "auquel modifier le classement : ")
            modify_elo_player(player_name)

        elif choice == 5:
            exit()
        else:
            print('Mauvais choix. Entrer un nombre entre 1 et 5\n')
