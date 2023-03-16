from colorama import Back
import random
from strenum import StrEnum
from enum import Enum, auto


ROW_LENGTH = 4


def test_pegs_colors(colors):
    """
    Tests if given list of colors is correct
    """
    colors = [color.upper() for color in colors]
    available_colors = ['RED', 'GREEN', 'YELLOW', 'BLUE']
    if len(colors) != ROW_LENGTH:
        raise InvalidAmountOfPegsError
    if not all(color in available_colors for color in colors):
        raise InvalidPegColorError


class InvalidGamemodeError(Exception):
    def __init__(self):
        super().__init__('Invalid gamemode, gamemode has to be an instance of the Gamemode class')


class InvalidPegColorError(Exception):
    def __init__(self):
        super().__init__('Invalid peg color. Color has to be either Red, Green, Yellow or Blue')


class InvalidKeyPegColorError(Exception):
    def __init__(self):
        super().__init__('Invalid key peg color. Color has to be either White, Cyan or Black')


class InvalidPegIndexError(Exception):
    def __init__(self):
        super().__init__(f'Invalid peg index. Index has to be either in range 1 - {ROW_LENGTH}')


class InvalidRoundsError(Exception):
    def __init__(self):
        super().__init__('Amount of rounds has to be between 1 and 10')


class InvalidAmountOfPegsError(Exception):
    def __init__(self):
        super().__init__(f'There are {ROW_LENGTH} pegs in total')


class Peg(StrEnum):
    RED = f'{Back.RED} {Back.RESET}'
    GREEN = f'{Back.GREEN} {Back.RESET}'
    BLUE = f'{Back.BLUE} {Back.RESET}'
    YELLOW = f'{Back.YELLOW} {Back.RESET}'
    WHITE = f'{Back.WHITE} {Back.RESET}'
    CYAN = f'{Back.CYAN} {Back.RESET}'
    BLACK = ' '


class Gamemode(Enum):
    PVP = auto()
    PVE = auto()
    PVE_SMART = auto()


class Player():
    """
    Class Player. Contains atributes:
    :param points: player's sum of points
    :type points: int
    :param name: player's name
    :type name: string
    """
    def __init__(self, name):
        self.points = 0
        self._name = name

    def __str__(self):
        return self._name

    def guess_pegs_colors(self, input=None):
        """
        Creates list of colors based on given input string (as guess)
        """
        colors = input
        test_pegs_colors(colors)
        return colors

    def code_pegs_colors(self, input=None):
        """
        Creates list of colors based on given input string (as coding)
        (In case of Player class, these two do the same thing)
        """
        return self.guess_pegs_colors(input)


class Bot(Player):
    def _create_random_peg_colors(self):
        """
        Chooses color code (randomly)
        """
        available_colors = ['RED', 'GREEN', 'YELLOW', 'BLUE']
        colors = []
        for _ in range(ROW_LENGTH):
            colors.append(random.choice(available_colors))
        return colors

    def guess_pegs_colors(self, input=None):
        """
        Creates list of random colors (as a guess)
        """
        colors = self._create_random_peg_colors()
        test_pegs_colors(colors)
        return colors

    def code_pegs_colors(self, input=None):
        """
        Creates list of random colors (as coding)
        """
        colors = self._create_random_peg_colors()
        test_pegs_colors(colors)
        return colors


class BotSmart(Bot):
    """
    Class BotSmart. Subclass of Player class. If it makes a move, the move is smart.
    :param points: bot's sum of points
    :type points: int
    :param name: bot's name
    :type name: string
    :param game: game in which BotSmart is participating
    :type game: Game
    """
    def __init__(self, name, game):
        super().__init__(name)
        self._game = game

    def guess_pegs_colors(self, input=None):
        """
        Chooses color code (with algorithm)
        """
        all_rows_colors = [row.colors for row in self._game.rows_list]
        possible_colors = ['RED', 'GREEN', 'BLUE', 'YELLOW']
        found = False
        for color in possible_colors:
            colors = [color] * ROW_LENGTH
            if colors not in all_rows_colors:
                found = True
                break
        if not found:
            colors = self.create_new_colors_variation(all_rows_colors)
        test_pegs_colors(colors)
        return colors

    def create_new_colors_variation(self, rows_colors):
        """
        Creates variation of game's coded row colors that does not exist in given rows_colors list
        """
        while True:
            colors = self._game.coded_row.colors
            random.shuffle(colors)
            if colors not in rows_colors:
                break
        return colors


class Row:
    """
    Class Row. Contains atributes:
    :param pegs: colors of pegs
    :type pegs: list of Color objects
    :param key_pegs: colors of key_pegs
    :type pegs: list of Color objects

    Takes a list of colors as an optional argument
    """
    def __init__(self, colors=None):
        self.set_pegs(colors)
        self._set_key_pegs()

    @property
    def pegs(self):
        """
        Returns list of Pegs
        """
        return self._pegs

    @property
    def colors(self):
        """
        Returns list of color names corresponding to Pegs in self._pegs
        """
        return list(map(self._peg_to_color, self._pegs))

    @property
    def key_pegs(self):
        """
        Returns list of key Pegs
        """
        return self._key_pegs

    @property
    def key_colors(self):
        """
        Returns list of color names corresponding key Pegs in self._key_pegs
        """
        return list(map(self._peg_to_color, self._key_pegs))

    def _color_to_peg(self, color):
        """
        Converts color name to Peg object
        """
        converter = {
            'BLACK': Peg.BLACK,
            'WHITE': Peg.WHITE,
            'RED': Peg.RED,
            'GREEN': Peg.GREEN,
            'BLUE': Peg.BLUE,
            'YELLOW': Peg.YELLOW,
            'CYAN': Peg.CYAN,
        }
        return converter[color]

    def _peg_to_color(self, peg):
        """
        Converts Peg object to color
        """
        converter = {
            Peg.BLACK: 'BLACK',
            Peg.WHITE: 'WHITE',
            Peg.RED: 'RED',
            Peg.GREEN: 'GREEN',
            Peg.BLUE: 'BLUE',
            Peg.YELLOW: 'YELLOW',
            Peg.CYAN: 'CYAN',
        }
        return converter[peg]

    def _set_peg(self, index, color):
        """
        Sets a color for peg pointed by index
        """
        color = color.upper()
        available_colors = ['RED', 'GREEN', 'YELLOW', 'BLUE']
        if index not in range(ROW_LENGTH):
            raise InvalidPegIndexError
        if color not in available_colors:
            raise InvalidPegColorError
        self._pegs[index] = self._color_to_peg(color)

    def __str__(self):
        """
        Returns string representation of a row (part of the board)
        """
        code_string = ''
        for peg in self._pegs:
            code_string += f'|  {peg * 2}  |'
        keys_string = ''
        for key in self._key_pegs:
            keys_string += f' {key}'
        inside = code_string + keys_string + ' |'
        border = '|' + '-' * ((ROW_LENGTH * 8) - 2) + '|' + '-' * (ROW_LENGTH * 2 + 1) + '|'
        return f'{border}\n{inside}\n{border}'

    def set_pegs(self, colors=None):
        """
        Sets row's color code to a code given by list of colors
        """
        self._pegs = [Peg.BLACK] * ROW_LENGTH
        if colors is not None:
            if len(colors) != ROW_LENGTH:
                raise InvalidAmountOfPegsError
            for index, color in enumerate(colors):
                self._set_peg(index, color)

    def _compare_pegs(self, other_row):
        """
        Compares pegs' colors of two rows. Returns a list of key pegs colors based on comparation
        """
        available_colors = ['RED', 'GREEN', 'YELLOW', 'BLUE', 'BLACK']
        same_color_and_placement = 0
        same_color = 0
        for index in range(ROW_LENGTH):
            if self._pegs[index] == other_row._pegs[index]:
                same_color_and_placement += 1
        for color in available_colors:
            if color in self.colors and color in other_row.colors:
                same_color += min(self.colors.count(color), other_row.colors.count(color))
        same_color_not_placement = same_color - same_color_and_placement
        white_colors = ['WHITE'] * same_color_and_placement
        cyan_colors = ['CYAN'] * same_color_not_placement
        black_colors = ['BLACK'] * (ROW_LENGTH - same_color_and_placement - same_color_not_placement)
        return white_colors + cyan_colors + black_colors

    def _set_key_peg(self, index, color):
        """
        Sets a color for key peg pointed by index
        """
        color = color.upper()
        available_colors = ['WHITE', 'CYAN', 'BLACK']
        if index not in range(ROW_LENGTH):
            raise InvalidPegIndexError
        if color not in available_colors:
            raise InvalidKeyPegColorError
        self._key_pegs[index] = self._color_to_peg(color)

    def _set_key_pegs(self, key_colors=None):
        """
        Sets row's key pegs to colors given in list
        """
        self._key_pegs = [Peg.BLACK] * ROW_LENGTH
        if key_colors is not None:
            if len(key_colors) != ROW_LENGTH:
                raise InvalidAmountOfPegsError
            for index, color in enumerate(key_colors):
                self._set_key_peg(index, color)

    def compare_pegs(self, other_row):
        """
        Compares row to other row and sets key pegs for the first one
        """
        key_colors = self._compare_pegs(other_row)
        self._set_key_pegs(key_colors)


class Game:
    """
    Class Game. Contains atributes:
    :param gamemode: gamemode number
    :type gamemode: int

    :param rounds: amount of rounds
    :type rounds: int

    :param rows_list: list of rows
    :type rows_list: list

    :param coded_row: Row coded in game
    :type coded_row: Row

    :param players_list: list of players
    :type players_list: list
    """
    def __init__(self, gamemode, rounds, amount_of_rows=10):
        if rounds not in range(1, 11):
            raise InvalidRoundsError
        self._gamemode = gamemode
        self._rounds = int(rounds)
        self._amount_of_rows = amount_of_rows
        self.coded_row = Row()
        self._create_players()
        self.new_board()

    @property
    def rounds(self):
        return self._rounds

    @property
    def amount_of_rows(self):
        return self._amount_of_rows

    @property
    def gamemode(self):
        return self._gamemode

    def board(self):
        """
        Returns board of rows. Row with the lowest index (0) is on the bottom
        """
        return reversed(self.rows_list)

    def _create_rows(self, amount):
        """
        Creates list of given amount of empty rows
        """
        return [Row() for _ in range(amount)]

    def _create_players(self):
        """
        Creates list of players based on game's gamemode
        """
        player1 = Player('Player 1')
        if self.gamemode == Gamemode.PVP:
            player2 = Player('Player 2')
        elif self.gamemode == Gamemode.PVE:
            player2 = Bot('Bot')
        elif self.gamemode == Gamemode.PVE_SMART:
            player2 = BotSmart('Bot Smart', self)
        else:
            raise InvalidGamemodeError
        self.players_list = [player1, player2]

    def is_guessed(self, row):
        """
        Checks if given row is the same as coded row
        """
        if row.pegs == self.coded_row.pegs:
            return True
        return False

    def player_give_points(self, player):
        """
        Gives points to a given player based on the number of rows needed to guess coded row
        """
        winning_row = None
        for row in self.rows_list:
            if self.is_guessed(row):
                winning_row = self.rows_list.index(row)
        if winning_row is None:
            points = self.amount_of_rows + 1
            player.points += points
        else:
            points = winning_row + 1
            player.points += points
        return points

    def winner(self):
        """
        Returns the winning player based on game players' points
        """
        player1, player2 = self.players_list
        if player1.points == player2.points:
            return None
        else:
            return (player1 if player1.points > player2.points else player2)

    def new_board(self):
        """
        Creates new, empty board (resets piervous one)
        """
        self.rows_list = self._create_rows(self.amount_of_rows)
