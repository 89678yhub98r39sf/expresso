"""
this file contains
"""

import networkx as nx

"""
description:
-
"""
def sample1():

    x = nx.Graph()

    # add the appropriate nodes
    for i in range(1,5):
        x.add_node(i)

    # add the appropriate edges
    x.add_edge(1,2)
    x.add_edge(2,3)
    x.add_edge(3,4)
    x.add_edge(1,4)

    return x

def sample2():

    x = nx.Graph()

    # add the appropriate nodes
    for i in range(1,5):
        x.add_node(i)

    # add the appropriate edges
    x.add_edge(1,2)
    x.add_edge(2,3)
    x.add_edge(3,4)
    x.add_edge(1,4)

    return x
