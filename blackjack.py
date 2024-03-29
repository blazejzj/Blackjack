import random

# Features to add:
# Add insurance if dealers first card == ace 


def deck_of_cards():
    """Function creating a shuffled deck of cards"""

    deck = []
    rank = range(2, 11)
    suit = ["Club", "Diamond", "Heart", "Spade"]
    figures = ["A", "K", "Q", "J"]

    # Generating all "number" cards in different suit
    for suits in suit:
        for ranks in rank:
            deck.append((suits, ranks))

    # Generating all "figure" cards in different suit
    for suits in suit:    
        for figure in figures:
            deck.append((suits, figure))

    # Shuffling the deck, returning shuffled deck 
    random.shuffle(deck)
    return deck

def get_card(deck):
    """Function for drawing a card"""
    card = deck.pop(0)
    return card

def get_value(hand):
    """Function for calculating card values"""
    eyes = 0
    aces_value = 0

    # Iterating through every card in hand and assigning the value
    for value in hand:
        card_value = value[1]
        if card_value in range(2, 11):
            eyes += card_value
        elif card_value in ["K", "J", "Q"]:
            eyes += 10
        else:
            eyes += 11
            aces_value += 1
    
    # If drawn ace busts -> change ace value to 1
    if eyes > 21 and aces_value > 0:
        eyes -= 10
        aces_value -= 1
    return eyes
    
def play_round(cash):
    """Function for one round of Blackjack"""
    get_insurance = 0 
    player_hand = []
    dealer_hand = []
    deck = deck_of_cards()

    print("\t==============Goodluck!==============\n")

    # 2 Starting cards for the player
    player_hand.append(get_card(deck))
    player_hand.append(get_card(deck))
    formatted_hand = ", ".join(f"{suit} {value}" for suit, value in player_hand)
    print(f"===Your hand: {formatted_hand}===\nYour eyes total {get_value(player_hand)}\n")

    # 2 Starting hands for the dealer -> Show first only
    dealer_hand.append(get_card(deck))
    if get_value(dealer_hand) == 11:
        while True:
            insurance = str(input("Dealers first card is an ace, would you like insurance? 100$\n(y/n)\t"))
            if insurance.lower() == 'y':
                cash = cash - 100
                get_insurance = 1
                break
            if insurance.lower() == 'n':
                get_insurance = 0
                break
            else:
                print("Invalid input!")
                continue
    suit, value = dealer_hand[0]
    print(f"===Dealers hand : {suit} {value}===\nDealers eyes total: {get_value(dealer_hand)}\n")
    dealer_hand.append(get_card(deck))

    # Player's turn
    while True:
            # Blackjack only if 2 initial cards equal to the value of 21
        if get_value(player_hand) == 21 and len(player_hand) == 2:
            print("===Player just got a BlackJack!===")
            cash = (cash * 2.5)
            return 'player', player_hand, dealer_hand, cash 

        elif get_value(player_hand) > 21:
            print("PLAYER BUSTED")
            cash = 0
            return 'dealer', player_hand, dealer_hand, cash
        else:
            stay_or_hit = input("\tWould you like to [S]tay, or [H]it?\n")
            if stay_or_hit.lower() == "h":
                player_hand.append(get_card(deck))
                suit, value = player_hand[-1]
                print(f"You have drawn {suit} {value}\nThe value: {get_value(player_hand)}")
            elif stay_or_hit.lower() == "s":
                break
            else:
                print("Invalid choice. Try again")

    # Dealer's turn
    while get_value(dealer_hand) <= 16:
        formatted_hand = ", ".join(f"{suit} {value}" for suit, value in dealer_hand)
        print(f"Dealers hand: {formatted_hand} and total eyes: {get_value(dealer_hand)}")
        # Dealer draws card if at 16 or below
        print("The dealer has to draw another card!\n")
        dealer_hand.append(get_card(deck))
        suit, value = dealer_hand[-1]
        print(f"Dealer has drawn: {suit} {value} with total eyes of: {get_value(dealer_hand)}")

    # Dealer blackjack check
    if get_value(dealer_hand) == 21 and len(dealer_hand) == 2:
        print("===Dealer just got a BlackJack!===")
        if get_insurance == 1:
            cash = cash
            print("You're insured, not cash has been lost!")
        else:
            cash = 0
            print("You're not insured! Cash lost!")
        return 'dealer', player_hand, dealer_hand, cash 

    # Dealer bust check
    elif get_value(dealer_hand) > 21:
        print(f"Dealer busted with {formatted_hand}\n")
        cash = (cash * 2)
        return 'player', player_hand, dealer_hand, cash

    # Check who won if nobody busts
    if get_value(player_hand) > get_value(dealer_hand):
        cash = (cash * 2)
        return 'player', player_hand, dealer_hand, cash # Player win, return also players/dealers ending cards
    elif get_value(player_hand) < get_value(dealer_hand):
        cash = 0
        return 'dealer', player_hand, dealer_hand, cash # Dealer win, return also players/dealers ending cards
    else:
        cash = cash
        return 'push', player_hand, dealer_hand, cash# Tie/Push, return also players/dealers ending cards

def main():
    # Starting cash
    total_cash = int(input("How much cash would you like to start with?\n$"))
    # Determine profit or loss
    total_earned_cash = total_cash  

    while True:
        if total_cash <= 0:
            print(f"You're out of cash! Current balance: ${total_cash}")
            print("Options:")
            print("[1] Add more money.")
            print("[2] Exit game.")
            choice = input("Enter your choice (1/2)\n")

            if choice == "1":
                added_cash = int(input("How much cash would you like to add?\n$"))
                total_cash += added_cash
                # Adding the amount to your total cash-in.
                total_earned_cash += added_cash 
            elif choice == "2":
                print("Thanks for playing!")
                print(f"Your total earned cash is: {total_earned_cash - total_cash}")
                exit()
            else:
                print("Invalid Input!")
                continue

        # The bet for each round
        bet = int(input(f"How much would you like to bet? (Available balance: {total_cash})\n$"))
        
        # If the bet exceeds available money, or is at 0 -> Invalid input
        if bet <= 0 or bet > total_cash:
            print("Invalid bet amount. Try again.")
            continue

        # Starting the rounds
        winner, player_hand, dealer_hand, win_amount = play_round(bet)

        # Result -> Prints out Players and Dealers hands
        formatted_player_hand = ", ".join(f"{suit} {value}" for suit, value in player_hand)
        formatted_dealer_hand = ", ".join(f"{suit} {value}" for suit, value in dealer_hand)
        print(f"\nPlayer's hand: {formatted_player_hand} (Total: {get_value(player_hand)})")
        print(f"Dealer's hand: {formatted_dealer_hand} (Total: {get_value(dealer_hand)})\n")

        if winner == 'player':
            print("Player wins this round!")
            print(f"You just won {win_amount - bet}$!\n") 
            total_cash += (win_amount - bet) 
        elif winner == 'dealer':
            print("Dealer wins this round!")
            print(f"You just lost {bet}\n")
            total_cash -= bet
        else:
            print("It's a push!\n")
            print(f"{bet} has been returned!")  

        print(f"Your total cash now is {total_cash}$!")
        print(f"Your total profit/loss is: {total_cash - total_earned_cash}$!") # Shows profit/loss

        while True:
            replay = input("Would you like to play another round? (y/n): ").lower()
            if replay in ['y', 'n']:
                break
            else:
                print("Invalid Input!")
                continue

        if replay == 'n':
            print("Thanks for playing!")
            print(f"Your total profit/loss is: {total_cash - total_earned_cash}")
            exit()

main()
