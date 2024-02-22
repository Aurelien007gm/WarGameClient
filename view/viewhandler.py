class ViewHandler:

    def __init__(self):

        self.isSelectingTerritoryForAttack = False
        self.isSelectingTerritoryForTransfer = False
        self.sourceTerritory = None
        self.destinationTerritory = None
        self.troop = None

    def Reset(self):
        self.isSelectingTerritoryForAttack = False
        self.isSelectingTerritoryForTransfer = False
        self.sourceTerritory = None
        self.destinationTerritory = None
        self.troop = None

    def SetSource(self,territoire):
        self.sourceTerritory = territoire

    def SetDestination(self,territoire):
        self.destinationTerritory = territoire


    def SetAttack(self):
        self.isSelectingTerritoryForAttack = True

    def SetTransfer(self,troop):
        self.isSelectingTerritoryForTransfer = True
        self.troop = troop

    