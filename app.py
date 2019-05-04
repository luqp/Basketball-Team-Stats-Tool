import constants
import os
import random


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


def show_menu_to_select():
    clean_screen()
    show_title()
    print(
        "Here are your choices:",
        "\n  1) Display Team Stats",
        "\n  2) Quit")

    return user_input()


def show_exit_message():
    print("\nStats tool closed... \U0001F6A7\n")


def show_team_stats(team, players):
    clean_screen()
    guardians = []

    for player in players:
        guardians.extend(player['guardians'])

    heights = [player['height'] for player in players]
    players_name = [player['name'] for player in players]
    experience = [player for player in players if player['experience']]
    inexperience = [player for player in players if not player['experience']]
    team_name = "Team:\n\033[1;37;44m {} Stats \033[0;m\n".format(team)

    print(
        team_name +
        "-" * 16, "\n" +
        "Total players:\n ",
        "{} \u2640\u2642\n".format(len(players)))
    print(
        "Players on Team:\n  "
        "{}".format(", ".join(players_name)), "\n")
    print(
        "\U0001F3C0 Total team experience:",
        "{}".format(len(experience)))
    print(
        "\U0001F3C0 Total team inexperience:",
        "{}".format(len(inexperience)))
    print(
        "\U0001F3C0 The team average height:",
        "{} inches".format(sum(heights)//len(heights)))
    print(
        "\nTeam's Guardians: \U0001F3C6\n ",
        "{}".format(", ".join(guardians)),
        "\n\n")


def keep_display_teams(keep):
    choice = None
    while choice != 'y':
        print("To continue selecting teams press the [y] key")
        print("To change team combination press the [c] key")
        print("Otherwise press the [n]o key:")
        choice = user_input()

        if choice == 'n':
            show_exit_message()
            keep = False
            break

        if choice == 'c':
            break

        clean_screen()
        show_title()

    return keep, choice


def obtain_players_data():
    players = []
    for origin in constants.PLAYERS:
        player = {}
        player['name'] = origin['name']
        experience = False if origin['experience'] == 'NO' else True
        guardians = origin['guardians'].split(" and ")
        height = int(origin['height'].split()[0])
        player['experience'] = experience
        player['guardians'] = guardians
        player['height'] = height
        players.append(player)
    
    return players


def distribute_players(teams):
    players = obtain_players_data()
    total_per_team = len(players) // len(teams)
    complete_teams = []

    for team in teams:
        enlisteds = []

        for number in range(total_per_team):
            not_enlisted = True

            while not_enlisted:
                player = random.choice(players)

                if player['experience'] == number % 2:
                    players.remove(player)
                    enlisteds.append(player)
                    not_enlisted = False

        team_players= team, enlisteds
        complete_teams.append(team_players)

    return complete_teams


def new_combination():
    teams = constants.TEAMS[:]
    players = distribute_players(teams)
    return teams, players


def start_tool():
    teams, complete_teams = new_combination()
    answers = ['1', 'display team', 'display']

    choice = None
    while choice not in answers:
        choice = show_menu_to_select()
        if choice == "2" or choice == "quit":
            show_exit_message()
            return

    keep = True
    while keep:
        try:
            show_teams(teams)
            picked = int(user_input()) - 1
        except ValueError:
            picked = None

        if picked in range(len(teams)):
            show_team_stats(*complete_teams[picked])
            keep, selection = keep_display_teams(keep)

            if selection == 'c':
                teams, complete_teams = new_combination()


if __name__ == "__main__":
    start_tool()
