from .accounttype import AccountType


class Account:
    """ An account either an ASSET, LIABILITY, INCOME, EXPENSES or GOOD account.
    It's value can be increase or decreased according to a double entry operation """
    def __init__(self, name, accountType, startingBalance=0) -> None:
        self.name = name
        self.accountType = accountType
        self.balance = startingBalance

    def debit(self, amount):
        """ A Debit is a positive change for ASSET and EXPENSES accounts, and negative for the rest. """
        if (self.accountType == AccountType.ASSET) or (self.accountType == AccountType.EXPENSES):
            self.balance += amount
        else:
            self.balance -= amount

    def credit(self, amount):
        """ A Credit is a negative change for ASSET and EXPENSES accounts, and positive for the rest. """
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
