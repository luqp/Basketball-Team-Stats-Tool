import constants
import os
import random
from pdb import set_trace

def clean_screen():
    os.system("cls" if os.name == "nt" else "clear")


def user_input():
    answer = input("\nEnter an option > ")
    return answer.lower()


def show_title():
    print("\U0001F525 BASKETBALL TEAM STATS TOOL\U0001F525\n")
    print("    ---- MENU ----\n")


def show_teams(teams):
    clean_screen()
    show_title()
    print("Select a team:")

    for team_numerate in enumerate(teams, 1):
        print("  {}) \u2B50 {}".format(*team_numerate))

    return teams


def show_menu_to_select():
    clean_screen()
    show_title()
    print(
        "Here are your choices:",
        "\n  1) Display Team Stats",
        "\n  2) Quit")

    return user_input()


def show_team_stats(team, players, guardians):
    clean_screen()
    phrase = "\nTeam: {} Stats \u26A1\n".format(team)
    players_name = [player['name'] for player in players]
    heights = [player['height'] for player in players]
    experience = [player for player in players if player['experience'] == "YES"]
    inexperience = [player for player in players if player['experience'] == "NO"]
    
    print(
        phrase,
        "-" * 15, "\n",
        "Total players: {}\n".format(len(players)))
    print(
        "Players on Team: ",
        " \U0001F3C3" * len(players), "\n"
        "  {}".format(", ".join(players_name)), "\n"
        )
    print("\U0001F3C0 Total team experience: {}".format(len(experience)))
    print("\U0001F3C0 Total team inexperience: {}".format(len(inexperience)))
    print("\U0001F3C0 The team average height: {}".format(get_average_height(heights)))
    print(
        "\nTeam's Guardians: \U0001F3C6\n",
        "  {}".format(", ".join(guardians)),
        "\n\n"
        )


def get_average_height(heights):
    sum_heights = 0

    for size in heights:
        height = size.split()
        sum_heights += int(height[0])
    
    return round(sum_heights / len(heights))


def distribute_players(teams):
    players = constants.PLAYERS[:]
    complete_teams = []

    exp = ["YES", "NO"]
    players_per_team = len(players) // len(teams)
    for team in teams:
        group = []
        guardians = []
        for i in range(players_per_team):
            not_selected = True
            
            while not_selected:
                player = random.choice(players)
                if player['experience'] == exp[i % len(exp)]:
                    group.append(player)
                    players.remove(player)
                    guardians.extend(player['guardians'].split(" and "))
                    not_selected = False

        team_players_guardians = team, group, guardians
        complete_teams.append(team_players_guardians)

    return complete_teams


def keep_display_teams():
    choice = None
    keep = True
    while choice != 'y':
        print(
            " To continue selecting teams press the [y] key\n",
            "To change team combination press the [c] key\n",
            "Otherwise press the [n]o key:")
        choice = user_input()

        if choice == 'n':
            print("\nStats tool closed... \U0001F6A7\n")
            keep = False
            break

        if choice == 'c':
            break
            
        clean_screen()

    return keep, choice
    

def new_combination():
    teams = constants.TEAMS
    players = distribute_players(teams)
    return teams, players


def start_tool():
    teams, complete_teams = new_combination()
    answers = ['1', 'y', 'display team', 'display']
    choice = None

    while choice not in answers:
        choice = show_menu_to_select() 
        if choice == "2" or choice == "quit":
            print("\nStats tool closed... \U0001F6A7\n")
            return

    keep =  True

    while keep:
        try:
            show_teams(teams)
            user_picked = user_input()
            picked = int(user_picked) - 1
        except ValueError:
            picked = None
            pass

        if picked in range(len(teams)):
            show_team_stats(*complete_teams[picked])
            keep, selection = keep_display_teams()

            if selection == 'c':
                teams, complete_teams = new_combination()

if __name__ == "__main__":
    start_tool()
