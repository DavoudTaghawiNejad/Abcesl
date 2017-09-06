def doubleEntry(debitAccount, creditAccount, amount):
    debitAccount.debit(amount)
    creditAccount.credit(amount)


class Contracts:
    def __init__(self):
        self.allAssets = []
        self.allLiabilities = []
