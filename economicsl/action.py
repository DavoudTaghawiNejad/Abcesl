class Action:
    def __init__(self, me) -> None:
        self.me = me
        self.amount = 0.0

    def perform(self) -> None:
        print("Model.actionsRecorder.recordAction(this); not called because deleted")

    def getAmount(self):
        return self.amount

    def setAmount(self, amount):
        self.amount = amount

    def getTime(self) -> int:
        return self.me.getTime()

    def print(self, actions=None) -> None:
        if actions:
            counter = 1
            for action in actions:
                print("Action", counter, "->", action.getName())
                counter += 1

    def getAgent(self):
        return self.me

    def getSimulation(self):
        return self.me.getSimulation()
