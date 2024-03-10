## manage all the call to server
import requests
import json
from player import Player, Animal
from territorymanager import TerritoryManager
from contract import Contract
from territory import (Territory,TerritoryMultiple,TerritoryCard,TerritoryElephant,
                       TerritoryGorilla,TerritoryAlpaga,TerritoryCoati,TerritoryYack,
                       TerritoryChacal,TerritoryLama,TerritoryCoq,TerritoryFennec,TerritoryHyena,
                       TerritoryKoala,TerritoryMacaque,TerritoryParesseux,TerritoryPenguin,TerritoryTaipan,
                       TerritoryTapir,TerritoryZebra)

class Server():
    def __init__(self):
        config = self.LoadConfig()
        self.ip = config.get("ip")
        ##self.server_url = 'http://192.168.1.64:8000'
        self.server_url = "http://" + self.ip + ":33800"
        self.playerid = int(input("Enter votre id : "))
        self.gamejson = self.GetGameJson()
        self.json = self.GetGameJson() # duplicate variable, to remove
        self.staticterritoriesjson = self.GetStaticTerritoriesJson()
        playerjson = self.gamejson["players"]
        self.players = []
        self.tm = None
        self.round = 1
        self.InitTerritories()
        terrjson = self.gamejson["territories"]
        for p in playerjson:
            kwargs = {"name": p["name"],"id":p["id"],"color": self.GetColor(p["id"]),"server":self}
            self.players.append(Player(**kwargs))


        for t in terrjson:
            id = t["id"]
            owner_id = t["owner_id"]
            
            owner = self.GetPlayerFromId(owner_id)
            troop = {"field":t["field"],"navy":t["navy"],"para":t["para"],"animals":t["animals"]}
            self.tm.territories[id].troop = troop
            self.tm.territories[id].owner_name = owner.name
            self.tm.territories[id].owner_id = owner_id
            self.tm.territories[id].owner = owner

        self.SetDataFromJson()

    def LoadConfig(self):
        try:
            with open('config.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}


    def GetGameJson(self):
        get_game_response = requests.get(f'{self.server_url}/get_game_json')
        game_json = get_game_response.json()
        return(game_json)
    
    def GetStaticTerritoriesJson(self):
        get_game_response = requests.get(f'{self.server_url}/get_territories_json')
        t_json = get_game_response.json()
        return(t_json)
    
    def GetLog(self):
        get_game_response = requests.get(f'{self.server_url}/get_log_json')
        l_json = get_game_response.json()
        return(l_json)

    
    def SetDataFromJson(self):
        playerjson = self.json["players"]

        for contract_json in self.json["contracts"]:
            player = self.GetPlayerFromId(contract_json["player_id"])
            contract_json["player"] = player
            contract = Contract(**contract_json)
            player.contract = contract




        for p in playerjson:
            id = p["id"]
            player = self.GetPlayerFromId(id)
            player.money = p["money"]
            contract_json = p.get("contract") or None
  
            if contract_json:
                contract_json["player"] = player
                contract = Contract(**contract_json)
                player.contract = contract
            else:
                player.contract = None
            
            player.contracts_draft = []
            print(("======================"))
            print(p["contracts_drawn"])
            for c in p["contracts_drawn"]:
                name = c.get("name")
                description = c.get("description")
                arg = c.get("arg")
                kwargs = {"name":name,"description":description,"arg":arg,"player":player}
                contract = Contract(**kwargs)
                player.contracts_draft.append(contract) 

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

            event_on = t["event_on"]
            event_countdown = t["event_countdown"]
            self.tm.territories[id].eventOn = event_on
            self.tm.territories[id].eventCountdown = event_countdown

    
    def GetUpdate(self):
        json = self.GetGameJson()
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
        if (id == -1):
            res = Animal()
        for p in self.players:
            if(p.id == id):
                res = p
        return(res)

    def GetColor(self,i):
        if(i==0):
            return(0,0,255)
        if(i==1):
            return(16,86,37)
        if(i==2):
            return(210,10,10)
        if(i==3):
            return(119,0,136)
    
    def ValidatePlay(self):
        print("Action valide pour ce joueur")
        req = {"action":"validate","player_id":self.playerid}
        response = requests.post(self.server_url,json = req)
        return(response)
    
    def Run(self):
        return(self.ValidatePlay())

    def Call(self,act):
        print("Envoie de la requete suivante :")
        myact =  act.GetJson()
        json_data = {"action":"action","acts":[myact]}
        response = requests.post(self.server_url, json=json_data)

    def InitTerritories(self,**kwargs):
        t = []
        animals = Animal()

        #for i in range(32):
            #t.append(Territory(**{"name": f"Jungle{i}","id":i ,"animals":animals}))
        ##t = kwargs["territories"]
        print(self.staticterritoriesjson)
        for terr in self.staticterritoriesjson:
            print(terr)
            t.append(Territory(**{"name":terr["name"],"id":terr["id"],"animals":animals,"effect":terr["effect"]}))
        # tri des territoires par id
        t.sort(key=lambda terr : terr.id)
        self.tm = TerritoryManager(territories = t)