import os
import time
from mastermind_classes import Player, Gamemode
from mastermind_classes import (
    InvalidPegColorError,
    InvalidAmountOfPegsError,
    InvalidRoundsError,
    test_pegs_colors
)


ROW_LENGTH = 4


class InvalidGamemodeNumberError(Exception):
    def __init__(self):
        super().__init__('Invalid gamemode number. Number has to be either 1, 2 or 3')


class IncorrectPlayerError(Exception):
    def __init__(self):
        super().__init__('Chosen player does not take part in the game')


def clear():
    """
    Uses correct clear command corresponding to user's OS
    """
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


def get_colors_from_user():
    """
    Tries to get colors of pegs from user input, handles possible errors
    """
    colors = None
    while True:
        try:
            colors = input().split(' ')
            test_pegs_colors(colors)
        except InvalidPegColorError:
            print('You have to choose between Red Green Blue or Yellow\n')
        except InvalidAmountOfPegsError:
            print(f'You have to pick exactly {ROW_LENGTH} colors\n')
        else:
            break
    return colors


def print_board(game):
    """
    Prints given game's board
    """
    for row in game.board():
        print(row)


def get_color_code(chosing_player):
    """
    Gets color code based on type of player
    """
    if type(chosing_player) == Player:
        print(f'{chosing_player}\nSet the color code:\n')
        player_input = get_colors_from_user()
        return chosing_player.code_pegs_colors(player_input)
    return chosing_player.code_pegs_colors()


def get_color_guess(guessing_player):
    """
    Gets color guess based on type of player
    """
    if type(guessing_player) == Player:
        print(f'{guessing_player}\nTry to guess the color code:\n')
        player_input = get_colors_from_user()
        return guessing_player.guess_pegs_colors(player_input)
    return guessing_player.guess_pegs_colors()


def play_turn(game, chosing_player, guessing_player):
    """
    Plays a turn of mastermind
    """
    clear()
    if chosing_player not in game.players_list or guessing_player not in game.players_list:
        raise IncorrectPlayerError
    game.new_board()
    color_code = get_color_code(chosing_player)
    game.coded_row.set_pegs(color_code)
    round_status = 'Lost'
    for row in game.rows_list:
        clear()
        print_board(game)
        print('')
        guess = get_color_guess(guessing_player)
        row.set_pegs(guess)
        row.compare_pegs(game.coded_row)
        if type(guessing_player) != Player:
            time.sleep(0.5)
        if game.is_guessed(row):
            round_status = 'Won'
            break
    clear()
    print_board(game)
    print('')
    points_given = game.player_give_points(chosing_player)
    point_or_points = 'point' if points_given == 1 else 'points'
    if round_status == 'Won':
        print(f'{guessing_player} guessed the code! {chosing_player} gets {points_given} {point_or_points}\n')
    else:
        print(f'CODED ROW:\n{game.coded_row}\n')
        print(f"{guessing_player} didn't manage to guess the code. {chosing_player} gets {points_given} {point_or_points}\n")


def print_points(player1, player2):
    """
    Prints players' points
    """
    print(f'Points:\n{player1}: {player1.points}\n{player2}: {player2.points}')


def print_winner(game):
    """
    Prints result of the game
    """
    if game.winner() is None:
        print('The game is tied, noone wins!')
    else:
        winner = game.winner()
        print(f'{winner} wins the game!')


def pick_gamemode_num():
    """
    Returns gamemode from input, handles possible errors
    """
    clear()
    menu = '1 -> Player vs player\n2 -> Player vs bot (easy)\n3 -> Player vs bot (hard)\n'
    print(menu + '\n\n')
    gamemode_num = 0
    while gamemode_num not in range(1, 4):
        try:
            gamemode_num = int(input('Choose a game mode: \n\n'))
            if gamemode_num not in range(1, 4):
                raise InvalidGamemodeNumberError
        except ValueError:
            clear()
            print(menu)
            print('Gamemode has to be a number\n')
        except InvalidGamemodeNumberError:
            clear()
            print(menu)
            print('Gamemode number has to be either 1, 2 or 3\n')
    return gamemode_num


def select_gamemode(gamemode_num):
    """
    Selects Gamemode variant based on gamemode number
    """
    if gamemode_num == 1:
        gamemode = Gamemode.PVP
    elif gamemode_num == 2:
        gamemode = Gamemode.PVE
    elif gamemode_num == 3:
        gamemode = Gamemode.PVE_SMART
    else:
        raise InvalidGamemodeNumberError
    return gamemode


def pick_gamemode():
    """
    Asks user for gamemode number and returns Gamemode variant based on it
    """
    gamemode_num = pick_gamemode_num()
    return select_gamemode(gamemode_num)


def pick_amount_of_rounds():
    """
    Returns amount of rounds from input, handles possible errors
    """
    clear()
    print('')
    rounds = 0
    while rounds not in range(1, 11):
        try:
            print('\n')
            rounds = int(input('Set an amount of rounds: \n\n'))
            if rounds not in range(1, 11):
                raise InvalidRoundsError
        except ValueError:
            clear()
            print('Amount of rounds has to be a number')
        except InvalidRoundsError:
            clear()
            print('Amount of rounds has to be between 1 and 10')
    return rounds


def print_rules():
    """
    Prints rules of Mastermind
    """
    sentence1 = 'Mastermind is a game between two players.'
    sentence2 = 'A codemaker sets a code, and a codebreaker tries to break it.'
    sentence3 = 'The codemaker has to set a code by choosing 4 colors between red, green, blue and yellow. Colors may repeat.'
    sentence4 = 'After every breaking attempt, the codebreaker will get a feedback based on his guess.'
    sentence5 = 'There will be one white indicator for every right color in a right spot, and cyan one for every right color in a wrong spot.'
    sentence6 = 'While setting or guessing the code, the player has to input it in a format "color color color color". Every color corresponds to one spot.'
    sentence7 = 'In every round, both players will have a chance to play as a codemaker and as a codebreaker.'
    sentence8 = "After every codebreaking sequence, points will be given to the codemaker based on the codebreaker's number of tries.\n"
    rules = [sentence1, sentence2, sentence3, sentence4, sentence5, sentence6, sentence7, sentence8]
    print('Rules:\n')
    for sentence in rules:
        print(sentence)
