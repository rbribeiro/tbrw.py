from __future__ import annotations
import random

class TBRW:
    """
    Tree Builder Random Walk (TBRW) is a simple model of a random walk on a growing tree. 
    """
    def __init__(self, p: float = 0.5, seed: int | None = None) -> TBRW:
        if not (0 <= p <= 1):
            raise ValueError(f"p must be between 0 and 1. Provided p={p!r}")
        self.p: float = p
        self.adj_list: list[list[int]] = [[0]]
        self.walker: int = 0
        self._rng =  random.Random(seed) 
    @property
    def num_nodes(self):
        return len(self.adj_list)

    def step(self):
        """Perform one step of the TBRW process."""
        # Coin flip
        if self._rng.random() <= self.p:
            new_node = self.num_nodes
            self.adj_list.append([self.walker])
            self.adj_list[self.walker].append(new_node)
        # Walker jump
        self.walker = self._rng.choice(self.adj_list[self.walker])

    def run(self, steps=10) -> list[list[int]]:
        """Run the TBRW process for a given number of steps."""
        for _ in range(steps):
            self.step()
        return self.adj_list

    def reset(self):
        """Reset the TBRW process to its initial state."""
        self.p = 0.5
        self.walker = 0
        self.adj_list = [[0]]
        self._rng = random.Random()

    def __repr__(self) -> str:
        return f"TBRW p= {self.p}, num_nodes= {self.num_nodes}, walker = {self.walker}"


tbrw = TBRW(1)

print(tbrw.run())
