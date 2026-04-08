"""Cache model: sets, blocks, and replacement policies."""


class CacheBlock:
    def __init__(self):
        self.valid = False
        self.tag = None
        self.last_used = 0  # for LRU tracking


class CacheSet:
    def __init__(self, associativity):
        self.blocks = [CacheBlock() for _ in range(associativity)]
        self.access_counter = 0

    def access(self, tag, policy="LRU"):
        """Return (hit: bool, evicted_tag: int|None)."""
        self.access_counter += 1

        # Check for hit
        for block in self.blocks:
            if block.valid and block.tag == tag:
                block.last_used = self.access_counter
                return True, None

        # Miss — find a victim
        victim = self._choose_victim(policy)
        evicted = victim.tag if victim.valid else None
        victim.valid = True
        victim.tag = tag
        victim.last_used = self.access_counter
        return False, evicted

    def _choose_victim(self, policy):
        # Prefer invalid blocks first
        for block in self.blocks:
            if not block.valid:
                return block
        if policy == "LRU":
            return min(self.blocks, key=lambda b: b.last_used)
        # FIFO / random fallback
        return self.blocks[0]


class Cache:
    def __init__(self, size_bytes, associativity, block_size, policy="LRU"):
        self.block_size = block_size
        self.associativity = associativity
        self.policy = policy

        num_sets = size_bytes // (associativity * block_size)
        self.sets = [CacheSet(associativity) for _ in range(num_sets)]

        self.hits = 0
        self.misses = 0

    def _index_and_tag(self, address):
        block_offset_bits = self.block_size.bit_length() - 1
        index_bits = len(self.sets).bit_length() - 1
        index = (address >> block_offset_bits) & ((1 << index_bits) - 1)
        tag = address >> (block_offset_bits + index_bits)
        return index, tag

    def access(self, address):
        index, tag = self._index_and_tag(address)
        hit, _ = self.sets[index].access(tag, self.policy)
        if hit:
            self.hits += 1
        else:
            self.misses += 1
        return hit

    @property
    def miss_rate(self):
        total = self.hits + self.misses
        return self.misses / total if total else 0.0
