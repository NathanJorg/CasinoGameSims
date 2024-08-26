from Blackjack import Blackjack

num_hands = 1
amount_bet = 0
amount_won = 0

for index in range(num_hands):
    if index % 10000 == 0 and index != 0:
        print('Hand',index,'Current RTP: ', round(amount_won/amount_bet,5))
    game = Blackjack(num_decks=1)
    game.play()    

    amount_bet += sum(game.player_bet)
    amount_won += game.amount_won   
    print(game.print_hand(game.dealer_hand))     
    print(game.print_hand(game.player_hands[0])) 

#print(amount_bet, ' ', amount_won, ' ', amount_won/amount_bet)

