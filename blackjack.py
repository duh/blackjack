from random import shuffle
from time import sleep

class Card:
    def __get_value(self):
        try:
            return int(self.rank)
        except:
            if self.rank == "A":
                return 11 # Special case - can be 1 or 11
            else:
                return 10 # All face cards are 10
                
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
        self.value = self.__get_value()

## Methods       
def new_deck() -> list[Card]:
    suits = ("♠", "♥", "♣", "♦")
    ranks = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "K", "Q", "J", "A")
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(Card(rank, suit))
    
    shuffle(deck)        
    return deck

def display_cards(deck: list[Card], quantity=0) -> None:
    cards = []
        
    if 0 < quantity < len(deck):
        deck = deck[:quantity]
    
    for card in deck:
        card_text = []
        card_text.append("┌───────────┐")
        card_text.append(f"│ {card.rank}         │")
        card_text.append("│           │")       
        card_text.append(f"│     {card.suit}     │")   
        card_text.append("│           │")
        card_text.append(f"│         {card.rank} │")     
        card_text.append("└───────────┘")      
        cards.append(card_text)
    
    for row in zip(*cards):
        print(" ".join(row))
    
def get_score(deck: list[Card]) -> int:
    score = 0
    aces = 0
    for card in deck:
        score += card.value
        if card.rank == "A":
            aces += 1
    
    for ace in range(aces):
        if score > 21:
            score -= 10           
    
    return score

def get_bet():
    while True:
        try:
            bet = int(input(f"You have ${balance}. How much would you like to bet?: $"))
            if bet > balance:
                print("Your bet cannot exceed your balance.")
            else: 
                if bet < 0:
                    print("Your bet cannot be negative.")
                else:
                    return bet

        except ValueError:
            print("You must specify a postive integer for your bet")    

def main() -> int: # Main game method, returns winnings/loss
    bet = get_bet() 
    
    ## Set up deck
    deck = new_deck()
    dealer_cards = [deck.pop(), deck.pop()]
    player_cards = [deck.pop(), deck.pop()]
    option = ""
    
    while option != "S": ## Main loop

        print("\nDealer's first card:")
        display_cards(dealer_cards, 1)
        print(f"Player's cards:")
        display_cards(player_cards)
        dealer_score = get_score(dealer_cards)
        player_score = get_score(player_cards)    
        print("\n--------------------------------")
        print(f"Your score: {player_score}")
        
        if(player_score == 21):
            print("--------------------------------\nYOU WIN!\nPerfect 21\n--------------------------------")
            return bet
        if(player_score > 21):
            print("--------------------------------\nDEALER WINS!\nYou went bust\n--------------------------------")
            return -bet
                
        while option.upper() != "H" and option.upper() != "S":
            option = input("Hit (H) or stand (S)?: ").upper()
        
        if(option == "H"):
            option = ""
            player_cards.append(deck.pop())
    
    print("\nDealer's cards:")
    display_cards(dealer_cards)
    while(dealer_score < 17):
        sleep(1)
        print("--------------------------------\nDealer hits!\n--------------------------------")
        dealer_cards.append(deck.pop())
        dealer_score = get_score(dealer_cards)
        print("\nDealer's cards:")
        display_cards(dealer_cards)
        
    print(f"Player's cards:")
    display_cards(player_cards)
    
    if(dealer_score > 21):
        print("--------------------------------\nYOU WIN!\nDealer went bust!\n--------------------------------")
        return bet
    if(player_score > dealer_score):
        print("--------------------------------\nYOU WIN!\n--------------------------------")
        return bet
    if(dealer_score > player_score):
        print("--------------------------------\nDEALER WINS!\n--------------------------------")
        return -bet   
    if(dealer_score == player_score):
        print("--------------------------------\nTIE!\n--------------------------------")    
        return 0   

    
balance = 100 
peak_balance = 0
biggest_win = 0
biggest_loss = 0
games_played = 0
        
while balance > 0:  
    winnings = main()
    games_played += 1            
    balance += winnings
    biggest_win = winnings if winnings > biggest_win else biggest_win
    biggest_loss = winnings if winnings < biggest_loss else biggest_loss
    peak_balance = balance if balance > peak_balance else peak_balance
    
print("--------------------------------\nBANKRUPT!\n--------------------------------")         
print(f"GAMES PLAYED: {games_played}")   
print(f"PEAK BALANCE: ${peak_balance}")
print(f"BIGGEST WIN: ${biggest_win}")   
print(f"BIGGEST LOSS: ${biggest_loss}")       
            
    