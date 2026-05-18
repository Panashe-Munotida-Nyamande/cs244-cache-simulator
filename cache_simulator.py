import math

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
        num_sets (int): How many sets.
        ways (int): How many lines per set (associativity).
        block_size (int): Size of each block in bytes.
        sets (list): The nested list structure holding all CacheLine objects.
        hits (int): Number of cache hits recorded.
        misses (int): Number of cache misses recorded.
    """

    def __init__(self, num_sets: int, ways: int, block_size: int):

        # Configuration
        self.num_sets = num_sets
        self.ways = ways
        self.block_size = block_size

        # Internal set structure
        self.sets = [[CacheLine() for _ in range(ways)] for _ in range(num_sets)]
        self.lru_order = [[] for _ in range(num_sets)]
        
        # Statistics
        self.hits = 0
        self.misses = 0

    def access(self, address):
        """Access the cache with a memory address.

        Computes the cache set index and tag from the given address, checks the
        corresponding set for a valid line with a matching tag, and updates
        hit/miss statistics.

        Args:
            address (int): The memory address being accessed.

        Returns:
            tuple[bool, list]: A tuple where the first element is True on a
            cache hit or miss (access succeeded), and the second element is the
            block data returned from the cache line.
        """

        # extract offset, index, tag from address
        offset_bits = int(math.log2(self.block_size))
        offset = address & (self.block_size - 1)

        index =(address >> offset_bits) & (self.num_sets - 1)
        index_bits = int(math.log2(self.num_sets))

        tag = address >> (offset_bits + index_bits)

        for way, line in enumerate(self.sets[index]):

            if line.valid and line.tag == tag:

                self.lru_order[index].remove(way)
                self.lru_order[index].append(way)

                self.hits += 1
                return True, line.data

        if len(self.lru_order[index]) == self.ways:
            way_to_use = self.lru_order[index][0]

        else:
            for way, line in enumerate(self.sets[index]):
                if not line.valid:
                    way_to_use = way
                    break

        simulated_data = [0] * self.block_size
        line_to_raplace = self.sets[index][way_to_use]

        line_to_raplace.valid = True
        line_to_raplace.tag = tag
        line_to_raplace.data = simulated_data

        if way_to_use in self.lru_order[index]:
            self.lru_order[index].remove(way_to_use)
        
        self.lru_order[index].append(way_to_use)

        self.misses += 1
        return False, simulated_data               #miss

if __name__ == "__main__":
    cache_object = Cache(4, 2, 16)

    # Fill set 3
    hit, data = cache_object.access(0xFFFF)
    print(f"Access 1 (0xFFFF) - Hit: {hit}")  # expect: False

    hit, data = cache_object.access(0x9FFF)
    print(f"Access 2 (0x9FFF) - Hit: {hit}")  # expect: False

    # Refresh 0xFFFF — makes it MRU
    hit, data = cache_object.access(0xFFFF)
    print(f"Access 3 (0xFFFF) - Hit: {hit}")  # expect: True

    # Force eviction — 0x9FFF should be evicted (LRU)
    hit, data = cache_object.access(0x2FFF)
    print(f"Access 4 (0x2FFF) - Hit: {hit}")  # expect: False