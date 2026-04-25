class CacheLine:
    """
    One line in a cache set

    Attributes:
        valid (bool): states whether the line is empty or holding real data
        tag (int): confirms whether what was found is what was being looked for
        data (list): actual bytes fetched from RAM

    """

    def __init__(self, valid = False, tag = 0, data = None):

        self.valid = valid
        self.tag = tag

        if data is None:
            self.data = []
        else:
            self.data = data

class Cache:
    """
    Holds the structure, handles memory access and tracks statistics

    Attributes:
        num_sets (int): how many set 
        associaticity (int): how many lines per set (ways)
        block_size (int): size of each block in bytes
    """

    def __init__(self, num_sets: int, ways: int, block_size: int):

        # Configuration
        self.num_sets = num_sets
        self.ways = ways
        self.block_size = block_size

        # Internal set structure
        self.sets = None
        
        # Statistics
        self.hits = 0
        self.misses = 0
