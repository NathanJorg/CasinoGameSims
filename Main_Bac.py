from Baccarat import Baccarat

from pathlib import Path

import os
import pandas as pd

def write_to_file(data, filename):
    df = pd.DataFrame(data)
    Path(filename).unlink(missing_ok=True)

    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
  
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(df.to_string(index=False))


def main():
    decks = 8
    num_hands = 100000000
    
    banker_win_total = 0.0
    player_win_total = 0.0
    tie_win_total = 0.0

    file_count = 1
    data = []


    for iter in range(1, num_hands+1):
        game = Baccarat(decks=decks, no_commission=False)
        game.play()

        banker_win, player_win, tie_win = game.winner_pay()
        banker_win_total += banker_win
        player_win_total += player_win
        tie_win_total += tie_win

        new_row = {
            'Hand': iter,
            'Banker hand': game.print_hand(game.banker_hand),
            'Player hand': game.print_hand(game.player_hand),
            'Banker value': game.hand_value(game.banker_hand),
            'Player value': game.hand_value(game.player_hand),
            'Banker win': banker_win,
            'Player win': player_win,
            'Tie win': tie_win
        }

        data.append(new_row)

        if iter % 500000 == 0:
            filename = f'.\\Baccarat Results\\baccarat_results_{file_count}.txt'

            write_to_file(data, filename)
            file_count += 1
            data = []
            print('Hand: ', iter)
            print(banker_win_total, ' ', player_win_total, ' ', tie_win_total)
            print(banker_win_total/iter, ' ', player_win_total/iter, ' ', tie_win_total/iter)

    if data:
        filename = f'.\\Baccarat Results\\baccarat_results_{file_count}.txt'
        Path(filename).unlink(missing_ok=True)
        write_to_file(data, filename)    
    
    print(banker_win_total, ' ', player_win_total, ' ', tie_win_total)
    print(banker_win_total/num_hands, ' ', player_win_total/num_hands, ' ', tie_win_total/num_hands)


if __name__ == "__main__":
    main()