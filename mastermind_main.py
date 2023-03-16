from mastermind_classes import Game
from mastermind_interface import (
    play_turn,
    print_points,
    print_winner,
    pick_gamemode,
    pick_amount_of_rounds,
    print_rules,
    clear
)


def main():
    clear()
    print_rules()
    input('Press enter to continue ')
    is_repeat = True
    while is_repeat:
        clear()
        gamemode = pick_gamemode()
        rounds = pick_amount_of_rounds()
        mastermind = Game(gamemode, rounds)
        player1, player2 = mastermind.players_list
        for _ in range(mastermind.rounds):
            play_turn(mastermind, player1, player2)
            print_points(player1, player2)
            input('\nPress enter to continue ')
            play_turn(mastermind, player2, player1)
            print_points(player1, player2)
            input('\nPress enter to continue ')
        clear()
        print_points(player1, player2)
        print('')
        print_winner(mastermind)
        print('')
        answear = input('If you want to play again, type "yes" ').upper()
        is_repeat = True if answear == 'YES' else False
    return


if __name__ == '__main__':
    main()
