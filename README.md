# tbrw.py – Tree Builder Random Walk

A minimal Python library for simulating **Tree Builder Random Walk** (TBRW):
a stochastic process that simultaneously grows a random tree and walks on it.

At each step:
1. With probability **p** a new leaf node is attached to the walker's
   current position.
2. The walker jumps to a uniformly-chosen neighbour of its current node.

## Installation

```bash
pip install tbrw
```

Or install directly from source:

```bash
git clone https://github.com/rbribeiro/tbrw.py.git
cd tbrw
pip install -e .
```

## Quick start

```python
from tbrw import TBRW

model = TBRW(p=0.5, seed=42)
adj = model.run(steps=100)

print(f"Nodes after 100 steps: {model.num_nodes}")
print(f"Walker is at node:     {model.walker}")
```

## API

### `TBRW(p=0.5, seed=None)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `p`       | `float` | Probability of growing a new leaf at each step (default `0.5`). |
| `seed`    | `int \| None` | Optional RNG seed for reproducibility. |

#### Methods

| Method | Description |
|--------|-------------|
| `step()` | Perform a single tbrw step. |
| `run(steps=10)` | Perform `steps` steps; returns the adjacency list. |
| `reset(seed=None)` | Reset to the initial single-node state. |

#### Properties

| Property | Description |
|----------|-------------|
| `num_nodes` | Current number of nodes in the tree. |
| `walker` | Index of the node the walker currently occupies. |

## License

MIT – see [LICENSE](LICENSE).
