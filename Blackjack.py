import random

players = []

#Card Object - Object for each card.
class Card:
    
    def __init__(self,suit,value):
        self.suit = suit #ie. Hearts, Diamonds etc.
        self.value = value #Value ie. Jack,1,7,Ace etc.
        self.description = "{} of {}".format(self.value,self.suit)

    #Worth is also stored as a variable. This differs to value as Jacks,
    #Kings, Queens and Aces will be given value. Used to work out a hand value.
        
    @property
    def worth(self):
        if isinstance(self.value, int): #Checks if value is integer.
            return [self.value]
        
        elif self.value == "Ace":
            return [1,11]
        
        else:
            return [10]

#Standard deck of cards.
class Deck:
    
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ["Spades","Clubs","Diamonds","Hearts"]:
            for number in range(2,11):
                self.cards.append(Card(suit,number))
            self.cards.append(Card(suit,"Ace"))
            self.cards.append(Card(suit,"Jack"))
            self.cards.append(Card(suit,"Queen"))
            self.cards.append(Card(suit,"King"))
        self.shuffle()

    def show(self):
        for card in self.cards:
            card.describe()

    def shuffle(self):
        random.shuffle(self.cards)

    def pick_card(self):
        return self.cards.pop()

    def reset(self):
        self.cards = []
        self.build()

class Dealer:
    def __init__(self,nickname):
        self.name = nickname
        self.clear_hand()

    def clear_hand(self):
        self.hand = []
        self.totals = [0]

    def pick(self,deck):
        self.hand.append(deck.pick_card())
        return self

    def show_one(self):
        print("\n"+self.name,"has:")
        #Listing one card
        print(self.hand[0].description)

    def show_hand(self,playing):
        if playing == True:
            print("\n"+self.name,"has:")
        #Listing each card
        for card in self.hand:
            print(card.description)
        

    def update_value(self):
        #Starting with the default hand value to be 0.
        #Totals is an array because an Ace will cause a hand to have multiple values.
        totals = [0]
        
        for card in self.hand:
            #Adding the total to each of the values
            totals = list(map(lambda x: x + card.worth[0],totals))
            #If the card is Ace
            if len(card.worth) == 2:
                #Then the length of totals will double - making room the the alternative
                #total(s).
                temp = list(map(lambda x: x + 10,totals))
                totals.extend(temp)
                
        totals = filter(lambda x: x<22,totals)
        self.totals = list(set(totals))

    def show_value(self):
        #Updating how much the hand is worth
        self.update_value()
        print("\n"+self.name+"'s hand is worth: ",end = "")
        
        for i in range(len(self.totals)):
            print(str(self.totals[i]),end = "")
            
            if len(self.totals)-1>i:
                print(" or ",end="")       
        print()

class Player(Dealer):

    def __init__(self,nickname,money):
        self.money = money
        self.pot = 0
        self.playing = True
        Dealer.__init__(self,nickname)

    def deposit(self):
        valid = False
        while not valid:
            deposit = input("How much would you like to deposit?\n$")
            try:
                deposit = int(deposit)
                if deposit <= self.money and deposit >0:
                    self.pot = deposit
                    valid = True
                    self.money -= self.pot
                else:
                    print("Error: Unable to deposit $"+deposit+". You have $"+self.money)
            except:
                print("Error: Integer not entered")
        print()
        

    def show_money(self):
        print(self.name +" has $"+str(self.money))
        
    def update_money(self,result):
        if result == "win":
            self.money += self.pot*2
        elif result == "push":
            self.money += self.pot

    def double_down(self):
        if self.money < self.pot:
            return False
        else:
            self.money -= self.pot
            self.pot = self.pot*2
            print(self.name,"has doubled down. His pot is now $"+str(self.pot))
            return True
        
            

class Game:
    def __init__(self,deck,players,dealer):
        self.players = players
        self.dealer = dealer
        self.deck = deck
        self.gameround = 1

        #Setting up hands
        #Two loops because each player gets dealt one card each before getting a second.
        for player in self.players:
            player.pick(self.deck)

        for player in self.players:
            player.pick(self.deck)
            player.update_value()


        self.dealer.pick(self.deck)
        self.dealer.pick(self.deck)

    def play_game(self):

        #Depositing funds
        for player in self.players:
            player.show_money()
            player.deposit()

        #Getting first cards and taking first turn
        for player in self.players:
            #Taking first turn
            player = self.make_choice(player)

        self.gameround += 1
        count = -1
        #While people are still playing
        while count != 0:
            count = 0
            for player in self.players:
                if player.playing == True:
                    player = self.make_choice(player)
                    if player.playing == True:
                        count += 1
            self.gameround += 1
        self.dealers_turn()
        print()

        #Results for game
        for player in self.players:
            if len(player.totals) == 0:
                print(player.name, "went bust and lost with the hand:")
            elif len(dealer.totals) == 0:
                print("Dealer went bust so",player.name,"won with the hand:")
                player.update_money("win")
            elif max(player.totals)>max(dealer.totals):
                print(player.name,"scored higher than the dealer and won with the hand:")
                player.update_money("win")
            elif max(player.totals)<max(dealer.totals):
                print(player.name,"scored less than the dealer and lost with the hand:")
            else:
                print(player.name,"scored the same as the dealer and pushed with the hand:")
                player.update_money("push")
            player.show_hand(False)
            print()

        
        return self.players



    def make_choice(self,player):

        print("========"+player.name+"'s Turn========")
        player.show_hand(True)
        player.show_value()
        self.dealer.show_one()
        
        #Checks if player has a 21
        if 21 in player.totals and self.gameround == 1:
            print("\n"+player.name,"was dealt a natural blackjack.")
            player.playing = False
            return player
        
        valid = False
        doubled = False
        
        while not valid:
            valid = True
            print("\nWhat would you like to do?:\n1- Hit\n2- Stand")
            if self.gameround == 1:
                print("3- Double down")
                #Split Function
                #if player1.hand[0].value == player1.hand[1].value:
                 #   print("4- Split")


            answer = input()
            if answer == "1":
                player = self.hit(player)

            elif answer == "2":
                player.playing = False

            elif answer == "3" and self.gameround == 1:
                doubled = player.double_down()
                if doubled:
                    player = self.hit(player)
                    player.playing = False
                    
                else:
                    print("Error: Unable to double down as you cannot afford it")
                    valid = False

            #elif answer == "4":
                  #self.split(player)

            else:
                print("Error: Invalid Input")
                valid = False
        print()
        return player


    def hit(self,player):  
        player.pick(self.deck)
        player.show_hand(True)
        player.update_value()
        
        if len(player.totals)== 0:
            print(player.name,"went bust!")
            player.playing = False
            
        elif 21 in player.totals:
            print(player.name,"has a blackjack!")
            player.playing = False
            
        
        else:
            player.show_value()
            
        return player


    def dealers_turn(self):
        self.dealer.update_value()
        while len(self.dealer.totals)!= 0:
            if max(self.dealer.totals)<17:
                self.dealer.pick(self.deck)
                self.dealer.update_value()
            else:
                break
        self.dealer.show_hand(True)
        if len(self.dealer.totals)==0:
            print("Dealer went bust!")
        else:
            dealer.show_value()


        
if __name__ == '__main__':

    #Getting number of players                      
    unanswered = True                           
    while unanswered:                          
        amount = input("How many people are playing?:\n")                       
        try:
            amount = int(amount)
            if amount > 7 or amount < 1:
                print("Error: Invalid Input\n")                  
            else:
                unanswered = False
                               
        except:
            print("Error: Invalid Input\n")

    
    for i in range(amount):
        name = input("\nEnter player "+str(i+1)+" name:\n")
        players.append(Player(name,100))
    print()
    
    dealer = Dealer("Dealer")
    
    while True:
        game = Game(Deck(),players,dealer)
        players = game.play_game()

        for player in players:
            if player.money == 0:
                print(player.name,"has no money left and has been kicked off the game")
                players.remove(player)
        if len(players) != 0:
            carryon = input("\nWould you like to play on? Y/N\n").lower()
            print()
            answered = False
        
            while not answered:
                if carryon == "n" or carryon == "no":
                    quit()
                    
                elif carryon == "y" or carryon == "yes":
                    answered = True
                    for player in players:
                        player.clear_hand()
                    dealer.clear_hand()
                    
                else:
                    print("Invalid Input")
                    
        else:
            print("Player(s) have no money left")

                
