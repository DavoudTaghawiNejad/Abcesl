from collections import defaultdict


class Contracts:
    """ Collection of all contracts an agent holds. Contracts can be on the
    asset or the liability side """
    def __init__(self):
        self.allAssets = defaultdict(list)
        """ contains all assets in a dictionary, with the assettype as a key """
        self.allLiabilities = defaultdict(list)
        """ contains all liabilities in a dictionary, with the assettype as a key """
