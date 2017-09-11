# This is the main class implementing double entry org.economicsl.accounting. All public operations provided by this class
# are performed as a double entry operation, i.e. a pair of (dr, cr) operations.
#
# A Ledger contains a set of accounts, and is the interface between an agent and its accounts. Agents cannot
# directly interact with accounts other than via a Ledger.
#
# At the moment, a Ledger contains an account for each type of contract, plus an equity account and a cash account.
#
# A simple economic agent will usually have a single Ledger, whereas complex firms and banks can have several books
# (as in branch banking for example).
from .contracts import Contracts
from .account import Account
from .accounttype import AccountType
from math import isclose

class Ledger:
    def __init__(self, me, inventory):
        """ A StressLedger is a list of accounts (for quicker searching)

        # Each Account includes an inventory to hold one type of contract.
        # These hashmaps are used to access the correct account for a given type of contract.
        # Note that separate hashmaps are needed for asset accounts and liability accounts: the same contract
        # type (such as Loan) can sometimes be an asset and sometimes a liability.

         A book is initially created with a cash account (it's the simplest possible book)
        """
        self.assetAccounts = {}  # a dict from a contract to a assetAccount
        self.inventory = inventory
        self.contracts = Contracts()
        self.goodsAccounts = {}
        self.liabilityAccounts = {}  # a dict from a contract to a liabilityAccount
        self.me = me

    def getAssetValue(self):
        """ Value of all assets and goods.
        Whether they are booked as assets or liabilities depends on the value at acquisition,
        not the current value """
        return (sum([aa.getBalance() for aa in self.assetAccounts.values()]) +
                sum([aa.getBalance() for aa in self.goodsAccounts.values()]))

    def getLiabilityValue(self):
        return sum([la.getBalance() for la in self.liabilityAccounts.values()])

    def getEquityValue(self):
        return self.getAssetValue() - self.getLiabilityValue()

    def getAssetValueOf(self, contractType):
        # return assetAccounts.get(contractType).getBalance();
        return sum((c.getValue() for c in self.contracts.allAssets[contractType]))

    def getLiabilityValueOf(self, contractType):
        # return liabilityAccounts.get(contractType).getBalance();
        return sum((c.getValue() for c in self.contracts.allLiabilities[contractType]))

    def getAllAssets(self):
        return [item for sublist in self.contracts.allAssets.values() for item in sublist]

    def getAllLiabilities(self):
        return [item for sublist in self.contracts.allLiabilities.values() for item in sublist]

    def getAssetsOfType(self, contractType):
        """ returns all contracts of a certain type that are booked as assets,
        whether they are booked as assets or liabilities depends on the value at acquisition,
        not the current value.
        """
        return self.contracts.allAssets[contractType]

    def getLiabilitiesOfType(self, contractType):
        """ returns all contracts of a certain type that are booked as liabilities,
        whether they are booked as assets or liabilities depends on the value at acquisition,
        not the current value.
        """
        return self.contracts.allLiabilities[contractType]

    def _addAccount(self, account, contractType):
        """ adds a new account """
        switch = account.getAccountType()
        if switch == AccountType.ASSET:
            assert contractType not in self.assetAccounts
            self.assetAccounts[contractType] = account
        elif switch == AccountType.LIABILITY:
            assert contractType not in self.liabilityAccounts
            self.liabilityAccounts[contractType] = account

        # Not sure what to do with INCOME, EXPENSES

    # Adding an asset means debiting the account relevant to that type of contract
    # and crediting equity.
    # @param contract an Asset contract to add
    def addAsset(self, contract):
        """ Adding an asset means debiting the account relevant to that type of contract
            and crediting equity.
            Args:

                contract:
                    an Asset contract to add """
        assetAccount = self.assetAccounts.get(type(contract))

        if assetAccount is None:
            # If there doesn't exist an Account to hold this type of contract, we create it
            assetAccount = Account(contract.getName(self.me), AccountType.ASSET)
            self._addAccount(assetAccount, type(contract))

        assetAccount.debit(contract.getValue())

        self.contracts.allAssets[type(contract)].append(contract)

    # Adding a liability means debiting equity and crediting the account
    # relevant to that type of contract.
    # @param contract a Liability contract to add
    def addLiability(self, contract):
        """ Adding a liability means debiting equity and crediting the account
            relevant to that type of contract.
            @param contract a Liability contract to add """
        liabilityAccount = self.liabilityAccounts.get(type(contract))

        if liabilityAccount is None:
            # If there doesn't exist an Account to hold this type of contract, we create it
            liabilityAccount = Account(contract.getName(self.me), AccountType.LIABILITY)
            self._addAccount(liabilityAccount, type(contract))

        liabilityAccount.credit(contract.getValue())

        # Add to the general inventory?
        self.contracts.allLiabilities[type(contract)].append(contract)

    def create(self, name, amount, value):
        self.inventory.create(name, amount)
        physicalthingsaccount = self.getGoodsAccount(name)
        physicalthingsaccount.debit(amount * value)

    def destroy(self, name, amount, value=None):
        if value is None:
            try:
                value = self.getPhysicalThingValue(name)
                self.destroy(name, amount, value)
            except:
                raise NotEnoughGoods(name, 0, amount)
        else:
            self.inventory.destroy(name, amount)
            self.getGoodsAccount(name).credit(amount * value)

    def getGoodsAccount(self, name):
        account = self.goodsAccounts.get(name)
        if account is None:
            account = Account(name, AccountType.GOOD)
            self.goodsAccounts[name] = account
        return account

    def getPhysicalThingValue(self, name):
        try:
            return self.getGoodsAccount(name).getBalance() / self.inventory.getGood(name)
        except:
            return 0.0

    # Reevaluates the current stock of phisical goods at a specified value and books
    # the change to org.economicsl.accounting
    def revalueGoods(self, name, value):
        old_value = self.getGoodsAccount(name).getBalance()
        new_value = self.inventory.getGood(name) * value
        if (new_value > old_value):
            self.getGoodsAccount(name).debit(new_value - old_value)
        elif (new_value < old_value):
            self.getGoodsAccount(name).credit(old_value - new_value)

    def addCash(self, amount) -> None:
        # (dr cash, cr equity)
        self.create("money", amount, 1.0)

    def subtractCash(self, amount) -> None:
        self.destroy("money", amount, 1.0)

    # Operation to pay back a liability loan; debit liability and credit cash
    # @param amount amount to pay back
    # @param loan the loan which is being paid back
    def payLiability(self, amount, loan):
        self.liabilityAccount = self.liabilityAccounts.get(loan)

        assert self.inventory.getCash() >= amount  # Pre-condition: liquidity has been raised.

        # (dr liability, cr cash )
        doubleEntry(self.liabilityAccount, self['money'], amount)

    def sell_asset(self, amount, asset):
        """ Books the sales of an asset.
        Args:
            amount:
                the *value* of the asset
        """
        assert amount <= asset.quantity
        asset.quantity -= amount
        if isclose(asset.quantity, 0):
            self.contracts.allAssets(type(asset)).remove(asset)
        assetAccount = self.assetAccounts[type(asset)]

        # (dr cash, cr asset)
        doubleEntry(self["money"], assetAccount, amount)

    # Operation to cancel a Loan to someone (i.e. cash in a Loan in the Assets side).
    #
    # I'm using this for simplicity but note that this is equivalent to selling an asset.
    # @param amount the amount of loan that is cancelled
    def pullFunding(self, amount, loan):
        loanAccount = self.getAccountFromContract(loan)
        # (dr cash, cr asset )
        doubleEntry(self.getCashAccount(), loanAccount, amount)

    def printBalanceSheet(self, me):
        print("Asset accounts:\n---------------")
        for a in self.assetAccounts.values():
            print(a.getName(), "-> %.2f" % a.getBalance())

        print("Breakdown: ")
        for c in self.contracts.allAssets:
            print("\t", c.getName(me), " > ", c.getValue())
        print("TOTAL ASSETS: %.2f" % self.getAssetValue())

        print("\nLiability accounts:\n---------------")
        for a in self.liabilityAccounts.values():
            print(a.getName(), " -> %.2f" % a.getBalance())
        for c in self.contracts.allLiabilities:
            print("\t", c.getName(me), " > ", c.getValue())
        print("TOTAL LIABILITIES: %.2f" % self.getLiabilityValue())
        print("\nTOTAL EQUITY: %.2f" % self.getEquityValue())

        print("\nSummary of encumbered collateral:")
        # for (Contract contract : getLiabilitiesOfType(Repo.class)) {
        #    ((Repo) contract).printCollateral();
        # }
        print("\n\nTotal cash: ", self.getGoodsAccount("cash").getBalance())
        # print("Encumbered cash: "+me.getEncumberedCash());
        # print("Unencumbered cash: " + (me.getCash_() - me.getEncumberedCash()));

    def getInitialEquity(self):
        return self.initialEquity

    def setInitialValues(self):
        self.initialEquity = self.getEquityValue()

    def getAccountFromContract(self, contract):
        return self.assetAccounts.get(contract)

    def getCashAccount(self):
        return self["money"]

    def devalueAsset(self, asset, delta_value):
        """ if an Asset loses value, I must debit equity and credit asset
        Args:
            asset

            delta_value:
                the value lost
        """
        self.assetAccounts[type(asset)].credit(delta_value)

        # Todo: perform a check here that the Asset account balances match the value of the assets. (?)

    def appreciateAsset(self, asset, delta_value):
        """ appreciates a certain asset
        Args:
            asset

            delta_value:
                the value gained
        """
        self.assetAccounts[type(asset)].debit(delta_value)

    def devalueLiability(self, liability, delta_value):
        """ devalues a certain liability
        Args:
            liability

            delta_value:
                the value lost
        """
        self.liabilityAccounts[type(liability)].debit(delta_value)

    def appreciateLiability(self, liability, delta_value):
        """ appreciates a certain liability
        Args:
            liability

            delta_value:
                the value gained
        """

        self.liabilityAccounts[type(liability)].credit(delta_value)



