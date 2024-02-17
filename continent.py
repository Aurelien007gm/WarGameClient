class Continent :

    def __init__(self,**kwargs):
        self.continent = {0:[0,1,2],1:[3,4,5,6,7],2:[8,9,10,11],3:[12,13,14,15]}
        self.continent_inverse = {}
        self.ComputeInverse()
        self.tm = kwargs.get("tm")

    def ComputeInverse(self):
        for continent, territories in self.continent.items():
            for t in territories:
                self.continent_inverse[t] = continent
            
    def HasContinent(self,player:int,t:int):
        res = True
        c = self.continent_inverse[t]
        for t_id in self.continent[c]:
            terr = self.tm.territories[t_id]
            if (terr.owner_id!= player):
                print(terr.id)
                print(terr.owner_id)
                print(player)

                res = False
                break
        return(res)