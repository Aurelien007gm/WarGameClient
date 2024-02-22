from card import Card
from player import Player,Animal
import random as rd
class Territory:



    def __init__(self,**kwargs):
        self.name = kwargs.get("name") or "Plaine des abysses"
        self.id = kwargs.get("id") or 0
        self.animals = kwargs.get("animals")
        self.owner = None
        self.owner_id =-1 # -1 is for animals
        self.owner_name="None"
        self.troop = {"field":0,"navy":0,"para":0,"animals":0}
        self.value = kwargs.get("value") or 500
        self.effect = "This territory has no effect"
        self.eventOn = False

    def ShowEffect(self):
        print(self.effect)

    


    

    
    def CountTroop(self):
        d = {2:"field",1:"navy",0:"para",-1:"animals"}
        nb = 0
            
        for w in range(-1,3):
            nb+= self.troop[d[w]]
        return(nb)
    
    def print(self):
        owner_name = "None" if self.owner is None else str(self.owner.name)
        print("Territory " + self.name + " is owned by player number " +owner_name + " and has :" + str(self.troop))
        #print(self.troop)

class TerritoryMultiple(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.effect ="Reward is multiplied by 1.05 each turn. Reset when owner changes"
      
    def SetOwner(self,p:Player):
        super().SetOwner(p)
        self.value = 500

    def EndTurn(self):
        self.value = int(self.value*1.05)
        super().EndTurn()

class TerritoryCard(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.effect ="Discard the worst card of the owner and draw another card each turn"

    def EndTurn(self):
        super().EndTurn()
        self.owner.DiscardCard()
        
class TerritoryGorilla(Territory):

        def __init__(self,**kwargs):
            super().__init__(**kwargs)
            self.effect ="If no attack from this territory, 20 percent of adding a bonus troop at the end of the turn"
        
        def EndTurn(self):
            print("Bonus troop on gorilla territory")
            if(not self.hasAttacked and rd.random()< 0.2 and self.owner !=-1):
                self.Deploy(field = 1)
            super().EndTurn()

class TerritoryAlpaga(Territory):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.effect ="No uprise of animals on this territory"
        self.upriseProbability = -1
        
class TerritoryCoati(Territory):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.effect ="Uprise can happens if troop are less or equal to 4"
        self.minTroopForUprise = 4

class TerritoryYack(Territory):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.value = 1000
        self.effect ="Reward is twice the normal price"

class TerritoryElephant(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.effect ="35 percent to attack with one more card"

    def SetMaxTroop(self, hasContinent = False):
        super().SetMaxTroop(hasContinent)

        if(rd.random() <= 0.35):
            self.maxTroopAttack += 1 
        return
    
class TerritoryZebra(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.effect ="50 percent to defend with one more card"

    def SetMaxTroop(self, hasContinent = False):
        super().SetMaxTroop(hasContinent)
        if(rd.random() <= 0.5):
            self.maxTroopDefense += 1 
        return
    
class TerritoryChacal(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.eventProb *= 0.33333
        self.effect ="Event are 3 times less likely on this territory"

class TerritoryTapir(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.eventProb *= 0.2
        self.effect ="Event are 5 times less likely on this territory."

class TerritoryPenguin(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.eventProb *= 3
        self.effect ="Event are 3 times more likely on this territory."

class TerritoryTaipan(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.eventProb *= 5
        self.effect ="Event are 5 times more likely on this territory."

class TerritoryCoq(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.eventReward *= 3
        self.effect ="Reward for event on this territory are 3 times higher than normal."

class TerritoryParesseux(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.maxAnimals = 5
        self.effect ="Animals defends this territory at 5 instead of 3."

class TerritoryLama(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.maxAnimals = 1
        self.effect ="Animals defends this territory at 1 instead of 3."

class TerritoryHyena(Territory):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.effect ="15 percent of cancel incoming attack."

    def CancelSpecial(self):
        probCancel = 0.15
        return(rd.random() < probCancel)
    

class TerritoryFennec(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.effectiveReward = self.value
        self.effect ="Reward is double if at least 5 territory at the beginning of the turn"

    def Begin(self):
        count = self.CountTroop()
        if count >= 5:
            self.effectiveReward = 2* self.value
        else:
            self.effectiveReward = self.value
        return
    
    def Reward(self):
        return(self.effectiveReward)

class TerritoryKoala(Territory):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.upriseProbability = 0.5
        self.effect ="50 percent of animal's uprise if this territory is only defended by a troop"
        

class TerritoryMacaque(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.effectiveReward = self.value
        self.effect ="No reward if less than 5 troop at the beginning of the turn"

    def BeforeEnd(self):
        count = self.CountTroop()
        if count >= 5:
            self.effectiveReward = self.value
        else:
            self.effectiveReward = 0
        return
    
    def Reward(self):
        return(self.effectiveReward)
    
class TerritoryMacaque(Territory):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.effectiveReward = self.value
        self.effect ="Reward is double if at least 5 territory at the beginning of the turn"

    def BeforeEnd(self):
        count = self.CountTroop()
        if count >= 5:
            self.effectiveReward = self.value
        else:
            self.effectiveReward = 0
        return
    
    def Reward(self):
        return(self.effectiveReward)
