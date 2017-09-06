from .accounttype import AccountType


class Account:
    def __init__(self, name, accountType, startingBalance=0.0) -> None:
        self.name = name
        self.accountType = accountType
        self.balance = startingBalance

    # A Debit is a positive change for ASSET and EXPENSES accounts, and negative for the rest.
    def debit(self, amount):
        if (self.accountType == AccountType.ASSET) or (self.accountType == AccountType.EXPENSES):
            self.balance += amount
        else:
            self.balance -= amount

    # A Credit is a negative change for ASSET and EXPENSES accounts, and positive for the rest.
    def credit(self, amount):
        if ((self.accountType == AccountType.ASSET) or (self.accountType == AccountType.EXPENSES)):
            self.balance -= amount
        else:
            self.balance += amount

    def getAccountType(self):
        return self.accountType

    def getBalance(self):
        return self.balance

    def getName(self):
        return self.name
