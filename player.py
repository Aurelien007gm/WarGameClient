import random as rd
from card import Card
from contract import Contract
from action import Action
class Player:

    def __init__(self,**kwargs):
        self.money = 5000
        self.name = kwargs.get("name") or "Unknown"
        self.id = kwargs.get("id") or 0
        self.color = kwargs.get("color") or (127,127,127)
        self.cards = []
        self.contract = None
        self.contracts_draft = []
        self.server = kwargs.get("server") or None
        for i in range(10):
            self.cards.append(Card())



    def AddMoney(self,nb):
        self.money+= nb
        if(nb < 0):
            for contract in self.contracts:
                # Fail contract that require to not spend money
                contract.Fail("MoneySpend")

    def print(self):
        print("Player "+ self.name +" has " + str(self.money) )
        print("Player Cards are " )
        for c in self.cards:
            c.print()

    def DiscardCard(self,cost = None):
        self.cards.sort(key=lambda t:t.attack + t.defense)
        print("Discard card")
        self.cards[0].print()
        self.cards[0] = Card()
        print("Get ")
        self.cards[0].print()
        if(cost):
            self.money -= cost

    def DrawCard(self):
        i = rd.randint(0,9)
        card = self.cards[i]
        self.cards[i] = Card()
        self.cards.sort(key=lambda t:t.attack + t.defense)
        return(card)
    
    def DrawContract(self,contract):
        self.contract = contract
        kwargs = contract.ToJson()

        act = Action("SetContract",**kwargs)
        act.print() # to remove, to debug
        self.server.Call(act)




    
class Animal(Player):

    def __init__(self,**kwargs):
        self.money = 0
        self.name = "animals"
        self.id = -1
        self.cards = []
        self.color = (200,200,100)

    def AddMoney(self,nb):
        return

    def print(self):
        print("Animals")

    def DiscardCard(self,cost = None):
        return

    def DrawCard(self):
        return(Card())