from typing import List

from .ledger import Ledger
from .obligations import ObligationMessage, ObligationsAndGoodsMailbox

from .obligations import Obligation
from .accounttype import AccountType  # NOQA
from abce import NotEnoughGoods  # NOQA
import abce


class Agent(abce.Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alive = True
        self.mainLedger = Ledger(self, self._haves)
        self.obligationsAndGoodsMailbox = ObligationsAndGoodsMailbox(self)
        self.simulation = kwargs['simulation_parameters']

    def _begin_subround(self):
        super()._begin_subround()
        self.step()

    def add(self, contract) -> None:
        if (contract.getAssetParty() == self.name):
            # This contract is an asset for me.
            self.mainLedger.addAsset(contract)
        elif (contract.getLiabilityParty() == self.name):
            # This contract is a liability for me
            self.mainLedger.addLiability(contract)
        else:
            print(contract, contract.getAssetParty(), contract.getLiabilityParty(), (self.name))
            raise Exception("who the fuck is this")

    def getName(self):
        return str(self.name)

    def getTime(self):
        return self.simulation.time

    def getSimulation(self):
        return self.simulation

    def isAlive(self) -> bool:
        return self.alive

    def addCash(self, amount) -> None:
        self.mainLedger.inventory.create('money', amount)

    def getCash_(self):
        return self.mainLedger.inventory['money']

    def getMainLedger(self) -> Ledger:
        return self.mainLedger

    def step(self) -> None:
        self.obligationsAndGoodsMailbox.step()

    def sendObligation(self, recipient, obligation: Obligation) -> None:
        if isinstance(obligation, ObligationMessage):
            self.message(recipient.group, recipient.id, '!oblmsg', obligation)
            self.obligationsAndGoodsMailbox.addToObligationOutbox(obligation)
        else:
            msg = ObligationMessage(self, obligation)
            self.message(recipient.group, recipient.id, '!oblmsg', msg)

    def printMailbox(self) -> None:
        self.obligationsAndGoodsMailbox.printMailbox()

    def message(self, receiver, topic, content, overload=None):

        if not isinstance(receiver, tuple):
            receiver = receiver.name
        super().message(receiver[0], receiver[1], topic, content)

    def get_obligation_outbox(self) -> List[Obligation]:
        return self.obligationsAndGoodsMailbox.getObligation_outbox()
