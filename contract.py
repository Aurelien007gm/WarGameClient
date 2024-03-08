class Contract:

    def __init__(self,**kwargs):
        self.description = kwargs.get("description") or "Basic contract"
        self.name = kwargs.get("name") or"Basic contract"
        self.player = kwargs.get("player") or None
        self.arg = kwargs.get("arg") or None
    


    def Print(self):
        print(f"Contract {self.name} is possed by {self.player.name}")

    def ToJson(self):
        json = {"contract_name":self.name,"description": self.description,"arg":self.arg,"player_id":self.player.id}
        return(json)






    