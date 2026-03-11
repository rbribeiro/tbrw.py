"""Tests for the tbrw package."""
import pytest

from tbrw import TBRW


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_default_construction():
    model = TBRW()
    assert model.p == 0.5
    assert model.num_nodes == 1
    assert model.walker == 0


def test_seed_reproducibility():
    a = TBRW(p=0.5, seed=0)
    b = TBRW(p=0.5, seed=0)
    assert a.run(50) == b.run(50)


def test_invalid_p_raises():
    with pytest.raises(ValueError):
        TBRW(p=1.5)
    with pytest.raises(ValueError):
        TBRW(p=-0.1)


# ---------------------------------------------------------------------------
# Growth behaviour
# ---------------------------------------------------------------------------

def test_p1_always_grows():
    """With p=1 every step should add a node."""
    model = TBRW(p=1.0, seed=7)
    model.run(steps=20)
    assert model.num_nodes == 21  # 1 initial + 20 new nodes


def test_p0_never_grows():
    """With p=0 the tree should stay at one node."""
    model = TBRW(p=0.0, seed=7)
    model.run(steps=20)
    assert model.num_nodes == 1


def test_run_returns_adj_list():
    model = TBRW(seed=1)
    adj = model.run(steps=10)
    assert isinstance(adj, list)
    assert all(isinstance(neighbours, list) for neighbours in adj)


# ---------------------------------------------------------------------------
# Adjacency list consistency
# ---------------------------------------------------------------------------

def test_adj_list_symmetry():
    """Every edge (u, v) must also appear as (v, u)."""
    model = TBRW(p=0.7, seed=99)
    adj = model.run(steps=50)
    for u, neighbours in enumerate(adj):
        for v in neighbours:
            assert u in adj[v], f"Missing back-edge {v} -> {u}"


# ---------------------------------------------------------------------------
# Step and reset
# ---------------------------------------------------------------------------

def test_step_increments_or_stays():
    model = TBRW(p=1.0, seed=5)
    before = model.num_nodes
    model.step()
    assert model.num_nodes == before + 1


def test_reset_clears_state():
    model = TBRW(seed=3)
    model.run(30)
    model.reset()
    assert model.num_nodes == 1
    assert model.walker == 0


def test_repr():
    model = TBRW(p=0.3)
    r = repr(model)
    assert "TBRW" in r
    assert "0.3" in r
