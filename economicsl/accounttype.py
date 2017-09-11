""" There are 5 account types in the AccountType class ASSET, LIABILITY, INCOME, EXPENSES, GOOD """
import enum


class AccountType(enum.Enum):
    ASSET=1
    LIABILITY=2
    INCOME=4
    EXPENSES=5
    GOOD=6
