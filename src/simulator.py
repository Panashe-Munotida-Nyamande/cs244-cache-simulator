"""Main simulation logic."""
from .cache import Cache
from .trace_parser import parse_trace


def run(trace_path, size_bytes, associativity, block_size, policy="LRU",
        ops=("L", "S", "M")):
    """Simulate a cache against a trace file.

    Returns a dict with hits, misses, and miss_rate.
    """
    cache = Cache(size_bytes, associativity, block_size, policy)

    for op, addr in parse_trace(trace_path):
        if op in ops:
            cache.access(addr)
            if op == "M":          # modify = load then store
                cache.access(addr)

    return {
        "hits": cache.hits,
        "misses": cache.misses,
        "miss_rate": cache.miss_rate,
        "total": cache.hits + cache.misses,
    }
