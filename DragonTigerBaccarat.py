from Baccarat import *
from WriteToFile import WriteToFile as wtf
from pathlib import Path
import sys

DRAGON_TIGER_PAYS = {
    'Six Card Dragon': 100,
    'Five Card Dragon': 40,
    'Four Card Dragon': 30,
}

BIG_DRAGON_PAYS = 31

SMALL_DRAGON_PAYS = 15

DRAGON_TIE_PAYS = 42


def hand_value(hand: BaccaratHand):
        return hand.hand_value
    
def number_of_cards(hand: BaccaratHand):
        return len(hand.card_ranks)

def main(verbose=False):

    num_decks = [6, 8]
    num_hands = 100000000

    for deck in num_decks:

        dragon_tiger_hits = {
            'Six Card Dragon': 0,
            'Five Card Dragon': 0,
            'Four Card Dragon': 0,        
        }

        big_dragon_hits = 0
        small_dragon_hits = 0
        dragon_tie_hits = 0

        if verbose:
            results = []
            file_count = 1
            header = ['Hand', 'Player Hand', 'Player Value', 'Banker Hand', 'Banker Value', 'Dragon Tiger Win', 'Big Dragon Win', 'Small Dragon Win', 'Dragon Tie Win']  

        for iteration in range(1, num_hands+1):
            game = Baccarat(decks=deck)
            game.play()

            if verbose:
                new_row = {
                    'Hand': iteration,
                    'Player Hand': game.player_hand,
                    'Player Value': game.player_hand.hand_value,
                    'Banker Hand': game.banker_hand,
                    'Banker Value': game.banker_hand.hand_value,  
                }

            # Dragon Tiger
            if hand_value(game.player_hand) == 7 and hand_value(game.banker_hand) == 6:
                if (number_of_cards(game.player_hand) + number_of_cards(game.banker_hand)) == 6:
                    dragon_tiger_hits['Six Card Dragon'] += 1
                    if verbose:
                        new_row['Dragon Tiger Win'] = DRAGON_TIGER_PAYS['Six Card Dragon']

                if (number_of_cards(game.player_hand) + number_of_cards(game.banker_hand)) == 5:
                    dragon_tiger_hits['Five Card Dragon'] += 1
                    if verbose:
                        new_row['Dragon Tiger Win'] = DRAGON_TIGER_PAYS['Five Card Dragon']

                if (number_of_cards(game.player_hand) + number_of_cards(game.banker_hand)) == 4:
                    dragon_tiger_hits['Four Card Dragon'] += 1
                    if verbose:
                        new_row['Dragon Tiger Win'] = DRAGON_TIGER_PAYS['Four Card Dragon']

            # Big Dragon
            if hand_value(game.player_hand) == 7 and number_of_cards(game.player_hand) == 3 and hand_value(game.player_hand) > hand_value(game.banker_hand):
                big_dragon_hits += 1
                if verbose:
                        new_row['Big Dragon Win'] = BIG_DRAGON_PAYS

            # Small Dragon 
            if hand_value(game.player_hand) == 7 and number_of_cards(game.player_hand) == 2 and hand_value(game.player_hand) > hand_value(game.banker_hand):
                small_dragon_hits += 1
                if verbose:
                        new_row['Small Dragon Win'] = SMALL_DRAGON_PAYS

            # Dragon Tie
            if hand_value(game.player_hand) == 7 and hand_value(game.banker_hand) == 7:
                dragon_tie_hits += 1
                if verbose:
                        new_row['Dragon Tie Win'] = DRAGON_TIE_PAYS

            if verbose:
                results.append(new_row)

            if iteration % 500000 == 0:
                print(
                    f'Decks: {deck}  Hand: {iteration}  '
                    f'Dragon Tiger RTP: {sum((DRAGON_TIGER_PAYS[k]+1) * dragon_tiger_hits[k] for k in DRAGON_TIGER_PAYS if k in dragon_tiger_hits) / iteration:.6f}  '
                    f'Big Dragon RTP: {(BIG_DRAGON_PAYS+1) * big_dragon_hits / iteration:.6f}  '
                    f'Small Dragon RTP: {(SMALL_DRAGON_PAYS+1) * small_dragon_hits / iteration:.6f}  '
                    f'Dragon Tie RTP: {(DRAGON_TIE_PAYS+1) * dragon_tie_hits / iteration:.6f}  '
                )     

                if verbose:
                    filename = f'.\\Dragon Tiger Results\\{deck} Decks\\results_{deck}_decks_{file_count}.txt'
                    filename_csv = f'.\\Dragon Tiger Results\\{deck} Decks\\results_{deck}_decks_{file_count}.csv'
                    wtf.write_to_file(results, filename, header)
                    wtf.write_to_csv(results, filename_csv, header)
                    file_count += 1
                    results = []


        print(
            f'Number of Decks: {deck}  Number of Hands: {num_hands}  '
            f'Dragon Tiger RTP: {sum((DRAGON_TIGER_PAYS[k]+1) * dragon_tiger_hits[k] for k in DRAGON_TIGER_PAYS if k in dragon_tiger_hits) / num_hands:.6f}  '
            f'Big Dragon RTP: {(BIG_DRAGON_PAYS+1) * big_dragon_hits / num_hands:.6f}  '
            f'Small Dragon RTP: {(SMALL_DRAGON_PAYS+1) * small_dragon_hits / num_hands:.6f}  '
            f'Dragon Tie RTP: {(DRAGON_TIE_PAYS+1) * dragon_tie_hits / num_hands:.6f}  '
        )
        print(f'Dragon Tiger Hit Rate: 1 in {int(num_hands / sum(dragon_tiger_hits[k] for k in dragon_tiger_hits))}')
        print(f'Big Dragon Hit Rate: 1 in {int(num_hands / big_dragon_hits)}') 
        print(f'Small Dragon Hit Rate: 1 in {int(num_hands / small_dragon_hits)}')
        print(f'Dragon Tie Hit Rate: 1 in {int(num_hands / dragon_tie_hits)}')
        print()
        print(f'Dragon Tiger Hit Rate (6 cards): 1 in {int(num_hands / dragon_tiger_hits["Six Card Dragon"])}')
        print(f'Dragon Tiger Hit Rate (5 cards): 1 in {int(num_hands / dragon_tiger_hits["Five Card Dragon"])}')
        print(f'Dragon Tiger Hit Rate (4 cards): 1 in {int(num_hands / dragon_tiger_hits["Four Card Dragon"])}')
        

        filename = f".\\Dragon Tiger Results\\simulation_results_{deck}_decks.txt"
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        Path(filename).unlink(missing_ok=True)

        with open(filename, "w") as f:
            sys.stdout = f
            print(
            f'Number of Decks: {deck}  Number of Hands: {num_hands}  '
            f'Dragon Tiger RTP: {sum((DRAGON_TIGER_PAYS[k]+1) * dragon_tiger_hits[k] for k in DRAGON_TIGER_PAYS if k in dragon_tiger_hits) / num_hands:.6f}  '
            f'Big Dragon RTP: {(BIG_DRAGON_PAYS+1) * big_dragon_hits / num_hands:.6f}  '
            f'Small Dragon RTP: {(SMALL_DRAGON_PAYS+1) * small_dragon_hits / num_hands:.6f}  '
            f'Dragon Tie RTP: {(DRAGON_TIE_PAYS+1) * dragon_tie_hits / num_hands:.6f}  '
            )
            print()
            print(f'Dragon Tiger Hit Rate: 1 in {int(num_hands / sum(dragon_tiger_hits[k] for k in dragon_tiger_hits))}')
            print(f'Big Dragon Hit Rate: 1 in {int(num_hands / big_dragon_hits)}') 
            print(f'Small Dragon Hit Rate: 1 in {int(num_hands / small_dragon_hits)}')
            print(f'Dragon Tie Hit Rate: 1 in {int(num_hands / dragon_tie_hits)}')
            print()
            print(f'Dragon Tiger Hit Rate (6 cards): 1 in {int(num_hands / dragon_tiger_hits["Six Card Dragon"])}')
            print(f'Dragon Tiger Hit Rate (5 cards): 1 in {int(num_hands / dragon_tiger_hits["Five Card Dragon"])}')
            print(f'Dragon Tiger Hit Rate (4 cards): 1 in {int(num_hands / dragon_tiger_hits["Four Card Dragon"])}')

            sys.stdout = sys.__stdout__

        if verbose and results:
            filename = f'.\\Dragon Tiger Results\\{deck} Decks\\results_{deck}_decks_{file_count}.txt'
            filename_csv = f'.\\Dragon Tiger Results\\{deck} Decks\\results_{deck}_decks_{file_count}.csv'
            wtf.write_to_file(results, filename, header)  
            wtf.write_to_csv(results, filename_csv, header) 

if __name__ == "__main__":
    main(verbose=False)