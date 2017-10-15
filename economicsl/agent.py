""" test """
from typing import List
from .ledger import Ledger
from .obligationmessage import ObligationMessage
from .obligationsmailbox import ObligationsMailbox
from .obligations import Obligation
from .accounttype import AccountType  # NOQA
from abce import NotEnoughGoods  # NOQA
import abce
from math import isclose


class Agent(abce.Agent):
    """ The abcesl.Agent inherits from abce.Agent, it additionally provides
    contracting and accounting capabilities """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alive = True
        self.mainLedger = Ledger(self, self._inventory)
        self.inventory = self.mainLedger.inventory
        self.obligationsMailbox = ObligationsMailbox(self)
        self.simulation = kwargs['simulation_parameters']

    def _begin_subround(self):
        """ This means step is called every new subround in ABCE, it's
        from the plugin API """
        super()._begin_subround()
        self._step()

    def add(self, contract):
        """ Adds a contract to the agent's ledger, figures out
        whether the contract is an asset or an liability """
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
        """ depreciated """
        return str(self.name)

    def getTime(self):
        """ depreciated """
        return self.simulation.time

    def getSimulation(self):
        return self.simulation

    def isAlive(self):
        return self.alive

    def addCash(self, amount):
        """ depreciated """
        self.create('money', amount, 1)

    def create(self, good, amount, value):
        """ Creates a good and books it into the according account with
        the value value

        Args:
            good

            amount

            value
        This function overwrites the abce.Agent's create function"""
        self.mainLedger.create(good, amount, value)

    def destroy(self, good, amount, value=None):
        """ deletes a good and books it into the according account.
        If no value is specified, the book value is calculated:
        account_value / number of goods.

        Args:
            good

            amount

            value (optional)

        This function overwrites the abce.Agent's delete function"""
        self.mainLedger.destroy(good, amount, value)

    def getCash_(self):
        """ depreciated """
        return self.mainLedger.inventory['money']

    def getMainLedger(self):
        """ depreciated """
        return self.mainLedger

    def _step(self):
        """ Processes received obligations """
        self.obligationsMailbox._step()

    def sendObligation(self, recipient, obligation):
        """ sends an obligation to an agent """
        if isinstance(obligation, ObligationMessage):
            self.send(recipient.group, '!oblmsg', obligation)
            self.obligationsMailbox.addToObligationOutbox(obligation)
        else:
            msg = ObligationMessage(self, obligation)
            self.send(recipient, '!oblmsg', msg)

    def printMailbox(self):
        """ Prints all obligations in the mailbox """
        self.obligationsMailbox.printMailbox()

    def message(self, receiver, topic, content):
        """ depreciated use ABCE's send method """
        if not isinstance(receiver, tuple):
            receiver = receiver.name
        super().send(receiver, topic, content)

    def get_obligation_outbox(self):
        """ Prints all obligations in the outbox """
        return self.obligationsMailbox.getObligation_outbox()

    def sell_asset(self, asset, quantity, value, price, receiver=None):
        """ Sells a quantity of an asset for a price. And books it
        accordingly. If no receiver is specified, the good is sold to
        a party outside of the model.
        """
        self.ledger.sell_asset(quantity, asset)




