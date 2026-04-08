"""Unit tests for the Cache class."""
import unittest
from src.cache import Cache


class TestCacheBasic(unittest.TestCase):
    def setUp(self):
        # 1 KB, direct-mapped, 64-byte blocks
        self.cache = Cache(size_bytes=1024, associativity=1, block_size=64)

    def test_cold_miss(self):
        self.assertFalse(self.cache.access(0x0))

    def test_hit_after_miss(self):
        self.cache.access(0x0)
        self.assertTrue(self.cache.access(0x0))

    def test_miss_rate(self):
        for addr in [0x0, 0x0, 0x40]:   # hit, miss
            self.cache.access(addr)
        self.assertAlmostEqual(self.cache.miss_rate, 2 / 3)


if __name__ == "__main__":
    unittest.main()
