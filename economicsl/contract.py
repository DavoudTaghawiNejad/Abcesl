class Contract:
    """ a contract must minimally implement the following functions"""
    def getAssetParty(self):
        """ Returns the asset party as a tuple (group, ID) e.G. ('bank', 5) """
        pass

    def getLiabilityParty(self):
        """ Returns the liability party as a tuple (group, ID) e.G. ('bank', 5) """
        pass

    def getValue(self, me):
        """ Returns the value of the contract conditional on the :code:`me` parameter.
        Me is a name tuple to determine, whether the valuating is from the perspective
        of the asset or liability side """
        pass

    def getAvailableActions(self, me):
        pass

    def getName(self, me):
        pass
