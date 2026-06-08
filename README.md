# cs244-cache-simulator

## Overview
This project is an architectural simulator designed to model and analyze low-level CPU cache behavior. The simulator reads a list of memory addresses one by one, breaks each address down to find where it should live in the cache, and checks if the data is already inside. It then records whether it found the data (a hit) or didn't (a miss) so you can see how efficient your cache setup is.
---

## How it Works
The simulator manages data eviction using a Least Recently Used (LRU) algorithm. This policy operates like a "recently used" stack on a small desk: when an address is accessed, it jumps to the top of the pile to remain immediately accessible. Because cache capacity is limited, once the architecture reaches full capacity and a cache miss occurs, the item at the very bottom—the one untouched for the longest duration—is evicted to make room for incoming data.

To map physical memory addresses to this tracking structure, the simulator parses each address into three component bitfields. The lengths of these fields are dynamically calculated based on the specific architectural constraints provided in the configuration file using the following foundational formulas:
```
offset bits = log₂(block size)
index bits = log₂(cache size ÷ (block size × associativity))
tag bits = N − (index bits + offset bits)
```
---

### Prerequisites
To execute the simulator, the following baseline environment is required:
* **Runtime:** Python 3.x (No external package dependencies required)
* **Operating System:** Cross-platform (Tested on Linux / Fedora Workstation)

### Input File Formats
The execution requires two distinct command-line configuration files: a cache architecture definition file and a memory reference trace file.

**Example config.txt:**
```text
# cache configuration
num_sets=4
ways=2
block_size=16
```

**Example trace.txt:**
```
# memory access trace
0xFFFF
0x9FFF
0xFFFF
0x2FFF
```

### Example Output
```
Accessing address 0xffff: Miss
Accessing address 0x9fff: Miss
Accessing address 0xffff: Hit
Accessing address 0x2fff: Miss
{'hit_rate': 0.25, 'miss_rate': 0.75, 'total_accesses': 4}
```
