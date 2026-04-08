"""Parse Valgrind lackey memory traces."""
import re

# Valgrind lackey line format:  I/L/S/M <hex_addr>,<size>
_TRACE_RE = re.compile(r"^\s*([ILSMilsm])\s+([0-9a-fA-F]+),(\d+)")


def parse_trace(path):
    """Yield (op, address) tuples from a lackey trace file.

    op is one of: 'I' (instruction), 'L' (load), 'S' (store), 'M' (modify).
    address is an integer.
    """
    with open(path) as f:
        for line in f:
            m = _TRACE_RE.match(line)
            if m:
                op = m.group(1).upper()
                addr = int(m.group(2), 16)
                yield op, addr
