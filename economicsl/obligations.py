class Obligation:
    def __init__(self, contract, amount, timeLeftToPay: int) -> None:
        self.amount = amount

        self.from_ = contract.getLiabilityParty()
        self.to = contract.getAssetParty()

        # there is only one simulation shared by all agents
        self.simulation = self.from_.getSimulation()
        self.timeToOpen = self.simulation.getTime() + 1
        self.timeToPay = self.simulation.getTime() + timeLeftToPay
        self.timeToReceive = self.timeToPay + 1

        assert self.timeToPay >= self.timeToOpen

        self.fulfilled = False

    def fulfil(self):
        pass

    def getAmount(self):
        return self.amount

    def isFulfilled(self) -> bool:
        return self.fulfilled

    def hasArrived(self) -> bool:
        return self.simulation.getTime() == self.timeToOpen

    def isDue(self) -> bool:
        return self.simulation.getTime() == self.timeToPay

    def getFrom(self):
        return self.from_

    def getTo(self):
        return self.to

    def setFulfilled(self) -> None:
        self.fulfilled = True

    def setAmount(self, amount) -> None:
        self.amount = amount

    def getTimeToPay(self) -> int:
        return self.timeToPay

    def getTimeToReceive(self) -> int:
        return self.timeToReceive

    def printObligation(self) -> None:
        print("Obligation from ", self.getFrom().getName(), " to pay ",
              self.getTo().getName(), " an amount ", self.getAmount(),
              " on timestep ", self.getTimeToPay(), " to arrive by timestep ",
              self.getTimeToReceive())


