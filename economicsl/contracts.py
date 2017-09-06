def doubleEntry(debitAccount, creditAccount, amount):
    debitAccount.debit(amount)
    creditAccount.credit(amount)

from collections import defaultdict

class Contracts:
    def __init__(self):
        self.allAssets = defaultdict(list)
        self.allLiabilities = defaultdict(list)
