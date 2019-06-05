import random


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

    def show_hand(self):
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
        Dealer.__init__(self,nickname)

    def deposit(self):
        valid = False
        while not valid:
            deposit = input("\nHow much would you like to deposit?")
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
        

    def show_money(self):
        print(self.name +" has $"+str(self.money))
        
    def update_money(self,result):
        if result == "win":
            self.money += self.pot*2
        elif result == "push":
            self.money += self.pot
        
            

class Game:
    def __init__(self,deck,player1,dealer):
        self.player1 = player1
        self.dealer = dealer
        self.deck = deck

        #Setting up hands
        self.dealer.pick(self.deck)
        self.dealer.pick(self.deck)

        self.player1.pick(self.deck)
        self.player1.pick(self.deck)
        self.player1.update_value()


    def play_game(self):

        self.player1.show_money()
        self.player1.deposit()
        self.dealer.show_one()
        self.player1.show_hand()
        self.player1.show_value()
        
        #Checks if player has a natural
        if 21 in self.player1.totals:
            print("\n"+self.player1.name,"was dealt a natural blackjack.")

            #Updating dealers value to see if he has a natural.
            self.dealer.update_value()
            self.dealer.show_hand()

            
            if 21 in self.dealer.totals:
                print("\nBoth dealer and player were dealt a natural.")
                print("Chips have been returned")
                self.push()
                
            else:
                self.win()
        else:
            bust = self.make_choice()
            if bust == True:
                print("\n"+self.player1.name,"went bust!")
                
            else:
                self.stand()
        return self.player1.money



    def make_choice(self):
        valid = False
        while not valid:
            answer = input("\nWould you like to hit or stand? H/S\n").lower()
            if answer == "hit" or answer == "h":
                bust = self.hit()
                if bust == True:
                    return True
                else:
                    valid = True
                    bust = self.make_choice()
                    return bust
            elif answer == "stand" or answer == "s":
                return False
            else:
                print("Invalid Input")

    def hit(self):
        self.player1.pick(self.deck)
        self.player1.show_hand()
        self.player1.update_value()
        
        if len(self.player1.totals)== 0:
            return True
        
        else:
            self.player1.show_value()
            return False

    def stand(self):
        self.dealer.update_value()
        
        while len(self.dealer.totals)!=0:
            
            if max(self.dealer.totals)<17:
                self.dealer.pick(self.deck)
                self.dealer.update_value()
                
            else:
                break
            
        self.dealer.show_hand()
        
        if len(self.dealer.totals)== 0:
            print("Dealer went bust!")
            self.win()
            return
        
        else:
            self.dealer.show_value()
            
        if max(self.dealer.totals)>max(self.player1.totals):
            self.lose()
            return
        
        elif max(self.dealer.totals)==max(self.player1.totals):
            self.push()
            return
        
        else:
            self.win()
            return

    def lose(self):
        print("You Lose!")


    def win(self):
        self.player1.update_money("win")
        print("You Won!")

    def push(self):
        self.player1.update_money("push")
        print("Push!")

        
if __name__ == '__main__':
    name = input("Enter player name:\n")
    print()
    
    player1,dealer =Player(name,100),Dealer("Dealer")
    
    while True:
        
        if player1.money != 0:
            game = Game(Deck(),player1,dealer)
            player1.money = game.play_game()
            carryon = input("\nWould you like to play on? Y/N\n").lower()
            answered = False
            
            while not answered:
                
                if carryon == "n" or carryon == "no":
                    quit()
                    
                elif carryon == "y" or carryon == "yes":
                    answered = True
                    player1.clear_hand()
                    dealer.clear_hand()
                    
                else:
                    print("Invalid Input")
                    
        else:
            print("You have no money left!")
            quit()
            
