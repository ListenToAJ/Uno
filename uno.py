import random
import os
import time
import copy

#~ Uno card class
class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color
    def __repr__(self): 
        return self.color + " " + self.value


#~ Globals Variables
number_of_players = 4
player_hands = [[] for _ in range(number_of_players)]
cards_per_hand = 7
game_direction = 1
current_player = 0
draw_amount = 0
delay = 1


#~ Functions
def shuffleCards(arr):
    random.shuffle(arr)

def playableCards(arr, top_card):
    #- Copy players hand into new list
    options = copy.deepcopy(arr)

    #- Top is wildcard (Only can happen at start)
    if top_card.color == "Black":
        return options
    
    #- Top is another special card
    if top_card.value == "Draw 4" and draw_amount > 0:
        returnArr = [obj for obj in options if obj.value == "Draw 4"]
        return returnArr
    elif top_card.value == "Draw 2" and draw_amount > 0:
        returnArr = [obj for obj in options if obj.value == "Draw 2"]
        return returnArr

    #- If no specific restrictions on top card
    check_num = 0
    while check_num != len(options):
        card_to_be_checked = options[check_num]
        #' If current card in hand is same color, face, or wildcard, leave it
        if card_to_be_checked.color == top_card.color or card_to_be_checked.value == top_card.value or card_to_be_checked.color == "Black":
            check_num += 1
            continue
        #' If card failed above test, it's not an option
        options.remove(card_to_be_checked)
    return options

def drawNCards(arr, n):
    #- Copy full deck and randomly take n cards from it, adding them to provided hand
    copy_deck = copy.deepcopy(full_deck)
    new_cards = random.sample(copy_deck, n)
    arr.extend(new_cards)


#~ Deck Building 
colors = ["Green", "Blue", "Yellow", "Red"]
full_deck = []

for color in colors:
    for i in range(0,13):
        #' Adding in cards 0-9, and 3 special cards for each color
        value = str(i)
        match i:
            case 10:
                value = "Skip"
            case 11:
                value = "Reverse"
            case 12:
                value = "Draw 2"
        full_deck.append(Card(value, color))

full_deck.append(Card("Wild", "Black"))
full_deck.append(Card("Wild", "Black"))
full_deck.append(Card("Draw 4", "Black"))
full_deck.append(Card("Draw 4", "Black"))

deck = copy.deepcopy(full_deck)
while(cards_per_hand*number_of_players > len(deck)):
    deck.extend(deck)

shuffleCards(deck)


#~ Giving cards to players
for i in range(0, cards_per_hand * number_of_players):
    playerChoice = i % 4
    player_hands[playerChoice].append(deck.pop())


#~ Gameplay
topCard = random.choice(full_deck)
while all(len(hand) > 0 for hand in player_hands):
    #- Round start
    print("\n###############################################\nTop card: " + str(topCard))

    #- YOUR TURN
    if(current_player == 0):
        print("\nYOUR TURN! \n\nYour cards: " + str(player_hands[0]))
        options = playableCards(player_hands[0], topCard)

        #' You have no options for cards
        if len(options) == 0:
            time.sleep(delay)
            #- If top card is draw 2 or 4, you must draw however many cards are stacked up
            if topCard.value[0:4] == "Draw" and draw_amount > 0:
                print("\nYou got hit! You must draw " + str(draw_amount))

                drawNCards(player_hands[current_player], draw_amount)
                draw_amount = 0

                print("Your new cards: " + str(player_hands[0]))
            #- If top card is anything else, simply draw 1 and keep going
            else:
                print("\nYou have no cards to play! Drawing one from deck")

                newCard = random.choice(copy.deepcopy(full_deck))
                player_hands[0].append(newCard)

                print("You drew " + str(newCard))
                print("Your new cards: " + str(player_hands[0]))
            time.sleep(delay)

        #' You do have atleast 1 card to play
        else:
            print("\nWhich card would you like to play?")

            #- Building input string with your options
            choiceString = ""
            for i in range(len(options)):
                choiceString += str(i+1) + ": " + str(options[i]) + ",  "
            choiceString = choiceString[:-3] + "\nYour choice: "
            
            #- Input validation
            while True:
                try: 
                    choice = int(input(choiceString))
                    if choice < 1 or choice > len(options):
                        raise ValueError("Choice is out of range")
                    break
                except ValueError:
                    print("Choice must be a number between 1 and " + str(len(options)) + "!")
                    print("\nTop card: " + str(topCard) + "\nYour cards: " + str(player_hands[0]))
                    print("\nWhich card would you like to play?")
                    
            #- You now have picked your card
            picked_card = options[choice-1]

            print("\nYou played: " + str(picked_card))
            player_hands[0] = [obj for obj in player_hands[0] if not (obj.value == picked_card.value and obj.color == picked_card.color) ]    # Remove picked card using list comprehension
            
            #- You picked a wildcard, now you need to pick the color + input validation
            while picked_card.color == "Black":
                picked_color = 0
                try: 
                    picked_color = int(input("\nWhat color would you like?\n1: Green, 2: Blue, 3: Yellow, 4: Red\n"))

                    if picked_color < 1 or picked_color > 4:
                        raise ValueError("Choice is out of range")
                    picked_card.color = colors[picked_color-1]
                except ValueError:
                    print("Choice must be a number between 1 and 4!")
                    print("\nYour cards: " + str(player_hands[0]))
            
            #- Special Cards
            if picked_card.value == "Draw 2" or picked_card.value == "Draw 4":
                draw_amount += int(picked_card.value[-1])                                # Set draw amount to either 2 or 4, this will affect next player
            elif picked_card.value == "Skip":
                current_player = (current_player + game_direction) % len(player_hands)  # Increment player count here, so that the regular increment player count later goes 1 further than normal
            elif picked_card.value == "Reverse":
                game_direction *= -1                                                    # Flip game direction so instead of going from player 2 to 3, you go from 2 to 1

            topCard = picked_card
        
        #' Move onto next player
        current_player = (current_player + game_direction) % len(player_hands)
    
    #- OPPONENTS TURN
    else:

        print("\nOPPONENT " + str(current_player) + "'S TURN!")
        opponent_options = playableCards(player_hands[current_player], topCard)

        print("\nThey have " + str(len(player_hands[current_player])) + " cards.")
        # print("\nTheir cards: " + str(player_hands[current_player]))
        # print("Their options: " + str(opponent_options))
        time.sleep(delay)

        #' Opponent has no options for cards
        if len(opponent_options) == 0:
            #- If top card is draw, they must draw however many cards are stacked up
            if topCard.value[0:4] == "Draw" and draw_amount > 0:
                print("\nOPPONENT " + str(current_player) + " MUST DRAW " + str(draw_amount))

                drawNCards(player_hands[current_player], draw_amount)
                draw_amount = 0

                # print("Their new cards: " + str(player_hands[current_player]))
            #- If top card is anything else, simply draw 1 and keep going
            else:
                print("\nOPPONENT " + str(current_player) + " MUST DRAW 1")

                drawNCards(player_hands[current_player], 1)
                
                # print("Their new cards: " + str(player_hands[current_player]))
        
        #' Opponent does have atleast 1 card to play
        else:
            #- Randomly pick a card from the options
            picked_card = random.choice(opponent_options)

            print("\nOPPONENT " + str(current_player) + " plays: " + str(picked_card))
            player_hands[current_player] = [obj for obj in player_hands[current_player] if not (obj.value == picked_card.value and obj.color == picked_card.color)]   # Remove picked card using list comprehension

            #- Special Cards
            if picked_card.color == "Black":
                picked_card.color = random.choice(colors)                                        # Randomly pick a color if they play a wildcard
                print("\nOPPONENT " + str(current_player) + " chooses " + picked_card.color)
            if picked_card.value == "Draw 2" or picked_card.value == "Draw 4":
                draw_amount += int(picked_card.value[-1])                                        # Set draw amount to either 2 or 4, this will affect the next player
                print("Next player must draw " + str(draw_amount))
            elif picked_card.value == "Skip":
                current_player = (current_player + game_direction) % len(player_hands)          # Increment player count here, so that the regular increment player count later goes 1 further than normal
            elif picked_card.value == "Reverse":
                game_direction *= -1                                                            # Flip game direction so instead of going from player 2 to 3, you go from 2 to 1

            topCard = picked_card
        input("Press enter to continue: ")                                                      # Wait for user to press enter to move to next turn
        
        #' Move onto next player
        current_player = (current_player + game_direction) % len(player_hands)  

#~ Win Message
print("\n\nWE HAVE A WINNER!\nCongratulations player #" + str(player_hands.index([])+1) + "!")
