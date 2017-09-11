import numpy as np
from abce import NotEnoughGoods
from .account import Account
from ledger import Ledger

def doubleEntry(debitAccount, creditAccount, amount: np.longdouble):
    debitAccount.debit(amount)
    creditAccount.credit(amount)

class Contracts:
    def __init__(self):
        self.allAssets = []
        self.allLiabilities = []


