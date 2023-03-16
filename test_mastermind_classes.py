from mastermind_classes import Row, Game, Player, Bot, BotSmart, Gamemode, Peg
from mastermind_classes import (
    InvalidPegColorError,
    InvalidAmountOfPegsError,
    InvalidRoundsError,
    InvalidGamemodeError,
    InvalidKeyPegColorError
)
from pytest import raises


def test_create_row_empty():
    row = Row()
    assert row.colors == ['BLACK'] * 4
    assert row.pegs == [Peg.BLACK] * 4


def test_create_row():
    row = Row(['Blue', 'Green', 'Yellow', 'Red'])
    assert row.colors == ['BLUE', 'GREEN', 'YELLOW', 'RED']


def test_create_row_wrong_color():
    with raises(InvalidPegColorError):
        Row(['Brown', 'Red', 'Green', 'Green'])


def test_create_row_wrong_too_much_colors():
    with raises(InvalidAmountOfPegsError):
        Row(['Red', 'Green', 'Green', 'Blue', 'Red'])


def test__create_rows():
    game = Game(Gamemode.PVP, 1)
    rows = game._create_rows(5)
    assert len(rows) == 5


def test_create_game():
    game = Game(Gamemode.PVP, 2)
    assert game.gamemode == Gamemode.PVP
    assert game.rounds == 2


def test_create_game_invalid_rounds():
    with raises(InvalidRoundsError):
        Game(3, 0)


def test_create_player():
    player = Player('Player')
    assert player.points == 0


def test_game_create_players_1():
    game = Game(Gamemode.PVP, 3)
    player1, player2 = game.players_list
    assert type(player1) == Player
    assert type(player2) == Player
    assert str(player1) == 'Player 1'
    assert str(player2) == 'Player 2'


def test_game_create_players_2():
    game = Game(Gamemode.PVE, 3)
    player1, player2 = game.players_list
    assert type(player1) == Player
    assert type(player2) == Bot
    assert str(player1) == 'Player 1'
    assert str(player2) == 'Bot'


def test_game_create_players_3():
    game = Game(Gamemode.PVE_SMART, 3)
    player1, player2 = game.players_list
    assert type(player1) == Player
    assert type(player2) == BotSmart
    assert str(player1) == 'Player 1'
    assert str(player2) == 'Bot Smart'


def test_game_create_players_error():
    with raises(InvalidGamemodeError):
        Game('3123123', 3)


def test_bot_code_pegs_color():
    bot = Bot('Bot')
    colors = bot.code_pegs_colors()
    assert len(colors) == 4
    assert all(color in ['RED', 'GREEN', 'BLUE', 'YELLOW'] for color in colors)


def test_player_code_pegs_color_incorrect_amount():
    with raises(InvalidAmountOfPegsError):
        Player('Plyer').code_pegs_colors(['red', 'green'])


def test_player_code_pegs_color_incorrect_color():
    with raises(InvalidPegColorError):
        Player('Player').code_pegs_colors(['Red', 'Yellow', 'Green', 'Brown'])


def test__compare_pegs_4_0():
    row1 = Row(['Red', 'Red', 'Red', 'Red'])
    row2 = Row(['Red', 'Red', 'Red', 'Red'])
    assert row1._compare_pegs(row2) == ['WHITE'] * 4


def test__compare_pegs_none():
    row1 = Row(['Blue', 'Blue', 'Blue', 'Blue'])
    row2 = Row(['Red', 'Red', 'Red', 'Red'])
    assert row1._compare_pegs(row2) == ['BLACK'] * 4


def test__compare_pegs_1_1():
    row1 = Row(['Red', 'Blue', 'Yellow', 'Blue'])
    row2 = Row(['Red', 'Yellow', 'Red', 'Red'])
    assert row1._compare_pegs(row2) == ['WHITE', 'CYAN', 'BLACK', 'BLACK']


def test__compare_pegs_0_4():
    row1 = Row(['Red', 'Blue', 'Yellow', 'Green'])
    row2 = Row(['Blue', 'Yellow', 'Green', 'Red'])
    assert row1._compare_pegs(row2) == ['CYAN'] * 4


def test__compare_pegs_2_2():
    row1 = Row(['Red', 'Blue', 'Yellow', 'Green'])
    row2 = Row(['Red', 'Yellow', 'Blue', 'Green'])
    assert row1._compare_pegs(row2) == ['WHITE'] * 2 + ['CYAN'] * 2


def test__compare_pegs_3_0():
    row1 = Row(['Red', 'Red', 'Blue', 'Blue'])
    row2 = Row(['Red', 'Red', 'Red', 'Blue'])
    assert row1._compare_pegs(row2) == ['WHITE'] * 3 + ['BLACK']


def test__set_key_pegs():
    row = Row()
    row._set_key_pegs(['WHITE', 'WHITE', 'CYAN', 'BLACK'])
    assert row.key_colors == ['WHITE', 'WHITE', 'CYAN', 'BLACK']


def test__set_key_pegs_error():
    row = Row()
    with raises(InvalidKeyPegColorError):
        row._set_key_pegs(['RED', 'WHITE', 'CYAN', 'BLACK'])


def test__set_key_pegs_none():
    row = Row()
    row._set_key_pegs()
    assert row.key_colors == ['BLACK'] * 4


def test_give_points_guessed_on_3():
    game = Game(Gamemode.PVP, 1)
    game.coded_row.set_pegs(['Red', 'Red', 'Red', 'Red'])
    game.rows_list[2].set_pegs(['Red', 'Red', 'Red', 'Red'])
    player1 = game.players_list[0]
    game.player_give_points(player1)
    assert player1.points == 3


def test_give_points_guessed_on_last():
    game = Game(Gamemode.PVP, 1)
    game.coded_row.set_pegs(['Red', 'Red', 'Red', 'Red'])
    game.rows_list[game.amount_of_rows - 1].set_pegs(['Red', 'Red', 'Red', 'Red'])
    player1 = game.players_list[0]
    game.player_give_points(player1)
    assert player1.points == game.amount_of_rows


def test_give_points_not_guessed():
    game = Game(Gamemode.PVP, 1)
    game.coded_row.set_pegs(['Red', 'Red', 'Red', 'Red'])
    player1 = game.players_list[0]
    game.player_give_points(player1)
    assert player1.points == 11


def test_winner():
    game = Game(Gamemode.PVP, 1)
    player1, player2 = game.players_list
    player1.points = 10
    player2.points = 9
    assert game.winner() == player1


def test_winner_tied():
    game = Game(Gamemode.PVP, 1)
    player1, player2 = game.players_list
    player1.points = 9
    player2.points = 9
    assert game.winner() is None


def test_is_guessed_true():
    game = Game(Gamemode.PVP, 1)
    game.rows_list[0].set_pegs(['Red', 'Red', 'Red', 'Red'])
    game.coded_row.set_pegs(['Red', 'Red', 'Red', 'Red'])
    assert game.is_guessed(game.rows_list[0]) is True


def test_is_guessed_false():
    game = Game(Gamemode.PVP, 1)
    game.rows_list[0].set_pegs(['Red', 'Red', 'Red', 'Red'])
    game.coded_row.set_pegs(['Green', 'Red', 'Red', 'Red'])
    assert game.is_guessed(game.rows_list[0]) is False
