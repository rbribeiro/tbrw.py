import random

import networkx as nx

from .utils import validate_probability, validate_steps


class TBRW:
    """Tree Builder Random Walk (TBRW) on a growing tree."""

    def __init__(self, p: float | list[float] = 0.5, s:int | None = None, seed: int | None = None) -> None:
        self.p: float | list[float] = validate_probability(p)
        self.adj_list: list[list[int]] = [[0]]
        self.walker: int = 0
        self._rng = random.Random(seed)
        self.height: int = 0
        self.steps_trajectory: list[int] = [0]
        self.distance_profile: list[int] = [0]
        self.s: int | None = validate_steps(s) if s is not None else None

    @property
    def num_nodes(self) -> int:
        """Total number of nodes in the current tree."""
        return len(self.adj_list)

    @property
    def degree_profile(self) -> list[int]:
        """The degree sequence of the current tree."""
        return [len(neighbors) for neighbors in self.adj_list]
    
    def _add_node(self)->None:
        new_node = self.num_nodes
        self.adj_list.append([self.walker])
        self.adj_list[self.walker].append(new_node)
        self.distance_profile.append(self.distance_profile[self.walker]+1)
        self.height = max(self.height, self.distance_profile[-1])

    def _jump(self)-> None:
        prev_walker_pos = self.walker
        self.walker = self._rng.choice(self.adj_list[self.walker])
        increment = self.distance_profile[self.walker] - self.distance_profile[prev_walker_pos]
        self.steps_trajectory.append(increment)


    def step(self, time: int = 1) -> None:
        """Perform one step of the TBRW process.

        The ``time`` argument is used as an index when ``p`` is a (periodic)
        probability sequence.
        """
        coin_param: float
        if isinstance(self.p, list):
            # cycle through p if the number of steps is larger than the list p
            coin_param = self.p[time % len(self.p)]
        else:
            coin_param = self.p

        # (1) Environment change step
        if self._rng.random() <= coin_param and (self.s is None or time % self.s == 0):
            self._add_node()

        # (2) Walker jump on (possibly) updated tree
        self._jump()

    def run(self, steps: int = 10) -> list[list[int]]:
        """Run the TBRW process for a given number of steps."""
        for i in range(steps):
            self.step(i)
        return self.adj_list

    def reset(self) -> None:
        """Reset the TBRW process to its initial state."""
        self.walker = 0
        self.adj_list = [[0]]
        self.height = 0
        self.steps_trajectory = [0]
        self.distance_profile = [0]

    def draw(self, **kwargs) -> None:
        """Draw the current tree with networkx drawing helpers."""
        graph = nx.from_dict_of_lists(dict(enumerate(self.adj_list)))
        nx.draw(graph, **kwargs)

    def __repr__(self) -> str:
        return (
            f"TBRW p:{self.p}, num_nodes:{self.num_nodes}, walker:{self.walker}, "
            f"current_distance: {self.distance_profile[self.walker]}, height: {self.height}"
        )
