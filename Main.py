from Blackjack import Blackjack

from pathlib import Path

import os
import numpy as np
import pandas as pd

import duckdb


MAX_HANDS = 2

num_hands = 10000
amount_bet = 0
amount_won = 0

player_header = []

for hand in range(MAX_HANDS):
    player_header.append('Hand_%s' % str(hand+1))
    player_header.append('Hand_value_%s' % str(hand+1))

headers = ['Hand'] + player_header + ['Dealer_hand'] + ['Dealer_value'] + ['Bet_amount'] + ['Win_amount']   


def write_to_file(data, filename):
    df = pd.DataFrame(data, columns=headers)
    df = df.replace(np.nan, '')

    Path(filename).unlink(missing_ok=True)

    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
   
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(df.to_string(index=False))

    # df_duck = pd.to_numeric(df['Dealer_value'], errors='coerce')
    # df_duck = df_duck.dropna()

    # print(df_duck)

    # lineitem = duckdb.query("SELECT * FROM df_duck WHERE Dealer_value>21")
    # print(lineitem)
    

data = []
file_count = 1

for iter in range(1, num_hands+1):
    game = Blackjack(num_decks=6, max_hands=MAX_HANDS, hit_on_soft_17=True)
    game.play()

    if game.check_blackjack(game.dealer_hand):
        dealer_value = 'BJ'
    elif game.hand_value(game.dealer_hand)[0] > 21:
        dealer_value = 'BUST'
    else:
        dealer_value = game.hand_value(game.dealer_hand)[0]

    new_row = {
        'Hand': iter,
        'Dealer_hand': game.print_hand(game.dealer_hand),
        'Dealer_value': dealer_value,
        'Bet_amount': sum(game.player_bet),
        'Win_amount': game.amount_won
    }

    for i in range(len(game.player_hands)):
        new_row['Hand_%s' % str(i+1)] = game.print_hand(game.player_hands[i])
        if game.check_blackjack(game.player_hands[i]) and len(game.player_hands) == 1:
            new_row['Hand_value_%s' % str(i+1)] = 'BJ'
        elif game.hand_value(game.player_hands[i])[0] > 21:
            new_row['Hand_value_%s' % str(i+1)] = 'BUST'
        else:
            new_row['Hand_value_%s' % str(i+1)] = game.hand_value(game.player_hands[i])[0]
   
    data.append(new_row)

    amount_bet += sum(game.player_bet)
    amount_won += game.amount_won

    if iter % 500000 == 0:
        print('Hand', iter, 'Current RTP: ', 1-(amount_bet-amount_won)/iter)
        filename = f'.\\Blackjack Results\\results_{file_count}.txt'
        write_to_file(data, filename)
        file_count += 1
        data = []
        

if data:
    filename = f'.\\Blackjack Results\\results_{file_count}.txt'
    write_to_file(data, filename)    

print(iter, ' ', amount_bet, ' ', amount_won, ' ', 1-(amount_bet-amount_won)/iter)