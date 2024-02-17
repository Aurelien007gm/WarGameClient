## manage all the call to server
import requests
import json
from player import Player, Animal
from territorymanager import TerritoryManager
from territory import (Territory,TerritoryMultiple,TerritoryCard,TerritoryElephant,
                       TerritoryGorilla,TerritoryAlpaga,TerritoryCoati,TerritoryYack,
                       TerritoryChacal,TerritoryLama,TerritoryCoq,TerritoryFennec,TerritoryHyena,
                       TerritoryKoala,TerritoryMacaque,TerritoryParesseux,TerritoryPenguin,TerritoryTaipan,
                       TerritoryTapir,TerritoryZebra)

class Server():
    def __init__(self):
        self.server_url = 'http://127.0.0.1:8000'
        self.id = int(input("Enter votre id : "))
        self.json = self.GetJson()
        playerjson = self.json["players"]
        self.players = []
        self.tm = None
        self.round = 1
        self.INIT()
        for p in playerjson:
            kwargs = {"name": p["name"],"id":p["id"],"color": self.GetColor(p["id"])}
            self.players.append(Player(**kwargs))

        terrjson = self.json["territories"]
        for t in terrjson:
            id = t["id"]
            owner_id = t["owner_id"]
            
            owner = self.GetPlayerFromId(owner_id)
            troop = {"field":t["field"],"navy":t["navy"],"para":t["para"],"animals":t["animals"]}
            self.tm.territories[id].troop = troop
            self.tm.territories[id].owner_name = owner.name
            self.tm.territories[id].owner_id = owner_id
            self.tm.territories[id].owner = owner


    def GetJson(self):
        get_game_response = requests.get(f'{self.server_url}/get_game_json')
        game_json = get_game_response.json()
        return(game_json)
    
    def SetDataFromJson(self):
        playerjson = self.json["players"]
        for p in playerjson:
            id = p["id"]
            player = self.GetPlayerFromId(id)
            player.money = p["money"]

        terrjson = self.json["territories"]
        for t in terrjson:
            id = t["id"]
            owner_id = t["owner_id"]
            
            owner = self.GetPlayerFromId(owner_id)
            troop = {"field":t["field"],"navy":t["navy"],"para":t["para"],"animals":t["animals"]}
            self.tm.territories[id].troop = troop
            self.tm.territories[id].owner_name = owner.name
            self.tm.territories[id].owner_id = owner_id
            self.tm.territories[id].owner = owner
    
    def GetUpdate(self):
        json = self.GetJson()
        round = json["turn"]
        if(round > self.round):
            self.json = json
            self.round = round
            print("Passage au round suivant")
            return(True)
        else:
            return(False)
    
    def GetPlayerFromId(self, id):
        res = None
        for p in self.players:
            if(p.id == id):
                res = p
        return(res)

    def GetColor(self,i):
        if(i==0):
            return(0,0,255)
        if(i==1):
            return(0,255,0)
        if(i==2):
            return(255,0,0)
        if(i==3):
            return(255,255,0)
    
    def ValidatePlay(self):
        req = {"action":"validate","player_id":self.id}
        response = requests.post(self.server_url,json = req)
        return(response)
    
    def Run(self):
        return(self.ValidatePlay())

    def Call(self,act):
        print("Envoie de la requete suivante :")
        myact =  act.GetJson()
        json_data = {"action":"action","acts":[myact]}
        response = requests.post(self.server_url, json=json_data)

    def INIT(self,**kwargs):
        t = []
        animals = Animal()
        """
        for i in range(16):
            if(i== 11):
                terr = TerritoryMultiple(**{"name": "Territoire des arbres centenaires "+str(i),"id": i,"animals":animals})
            elif(i==8):
                terr = TerritoryCard(**{"name": "Territoire de la nuit sans fin "+str(i),"id": i,"animals":animals})
            elif(i==15):
                terr = TerritoryGorilla(**{"name": "Territoire de la jungle sauvage "+str(i),"id": i,"animals":animals})
            elif(i==9):
                terr = TerritoryAlpaga(**{"name": "Territoire du vaste Salar "+str(i),"id": i,"animals":animals})
            elif(i==6):
                terr = TerritoryCoati(**{"name": "Territoire du vaste Salar "+str(i),"id": i,"animals":animals})
            elif(i==4):
                terr = TerritoryYack(**{"name": "Territoire des collines verdiyante "+str(i),"id": i,"animals":animals})
            elif(i==2):
                terr = TerritoryElephant(**{"name": "Territoire des volcants étincelants "+str(i),"id": i,"animals":animals})
            else:
                terr = Territory(**{"name": "Jungle "+str(i),"id": i,"animals":animals})
            t.append(terr)"""
        
        t.append(Territory(**{"name": "Jungle 0","id":0 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 1","id":1 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 2","id":2 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 3","id":3 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 4","id":4 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 5","id":5 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 6","id":6 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 7","id":7 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 8","id":8 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 9","id":9 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 10","id":10 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 11","id":11 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 12","id":12 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 13","id":13 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 14","id":14 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 15","id":15 ,"animals":animals}))
        ##t = kwargs["territories"]
        self.tm = TerritoryManager(territories = t)