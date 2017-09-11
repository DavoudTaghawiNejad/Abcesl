
class ObligationsMailbox:
    def __init__(self, owner) -> None:
        self.obligation_unopened = []
        self.obligation_outbox = []
        self.obligation_inbox = []
        self.obligationMessage_unopened = []
        self.obligationMessage_inbox = []
        self.goods_inbox = []
        self.owner = owner


    def addToObligationOutbox(self, obligation) -> None:
        self.obligation_outbox.append(obligation)

    def getMaturedObligations(self):
        return sum([o.getAmount() for o in self.obligation_inbox if o.isDue() and not o.isFulfilled()])

    def getAllPendingObligations(self):
        return sum([o.getAmount() for o in self.obligation_inbox if not o.isFulfilled()])

    def getPendingPaymentsToMe(self):
        return sum([o.getAmount() for o in self.obligation_outbox if o.isFulfilled()])

    def fulfilAllRequests(self) -> None:
        for o in self.obligation_inbox:
            if not o.isFulfilled():
                o.fulfil()

    def fulfilMaturedRequests(self) -> None:
        for o in self.obligation_inbox:
            if o.isDue() and not o.isFulfilled():
                o.fulfil()

    def step(self) -> None:
        self.obligation_inbox.extend(self.owner.get_messages('!oblmsg'))
        # Remove all fulfilled requests
        self.obligation_inbox = [o for o in self.obligation_inbox if not o.isFulfilled()]
        self.obligation_outbox = [o for o in self.obligation_outbox if not o.isFulfilled()]

        # Remove all requests from agents who have defaulted.
        # TODO should be in model not in the library
        self.obligation_outbox = [o for o in self.obligation_outbox if o.getFrom().isAlive()]

        # Move all messages in the obligation_unopened to the obligation_inbox
        self.obligation_inbox += [o for o in self.obligation_unopened if o.hasArrived()]
        self.obligation_unopened = [o for o in self.obligation_unopened if not o.hasArrived()]

        # Remove all fulfilled requests
        self.obligationMessage_inbox = [o for o in self.obligationMessage_inbox if not o.is_read()]

        # Move all messages in the obligation_unopened to the obligation_inbox
        self.obligationMessage_inbox += list(self.obligationMessage_unopened)
        self.obligationMessage_unopened = []

        # Remove all fulfilled requests
        assert not self.goods_inbox

        # Move all messages in the obligation_unopened to the obligation_inbox

    def printMailbox(self) -> None:
        if ((not self.obligation_unopened) and (not self.obligation_inbox) and
           (not self.obligation_outbox)):
            print("\nObligationsAndGoodsMailbox is empty.")
        else:
            print("\nObligationsAndGoodsMailbox contents:")
            if not (not self.obligation_unopened):
                print("Unopened messages:")
            for o in self.obligation_unopened:
                o.printObligation()

            if not (not self.obligation_inbox):
                print("Inbox:")
            for o in self.obligation_inbox:
                o.printObligation()

            if not (not self.obligation_outbox):
                print("Outbox:")
            for o in self.obligation_outbox:
                o.printObligation()
            print()

    def getMessageInbox(self):
        return self.obligationMessage_inbox

    def getObligation_outbox(self):
        return self.obligation_outbox

    def getObligation_inbox(self):
        return self.obligation_inbox
