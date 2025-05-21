import pytest
from javineitor.main import create_graph

def test_create_graph():
    graph = create_graph()
    assert graph is not None

def test_add_node():
    graph = create_graph()
    graph.add_node("A", label="Test")
    assert "A" in graph.nodes

def test_add_edge():
    graph = create_graph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_edge("A", "B")
    assert ("A", "B") in graph.edges 