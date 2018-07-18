# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 21:51:31 2018

@author: stef_leonA
"""
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3)])
G.add_edge(2,1)
G.add_node("spam")       # adds node "spam"
print(list(nx.connected_components(G)))

nx.draw(G)
#nx.draw_random(G)
#nx.draw_spectral(G)
plt.show()


#[set([1, 2, 3]), set(['spam'])]
#sorted(d for n, d in G.degree())
#[0, 1, 1, 2]
#nx.clustering(G)
#{1: 0, 2: 0, 3: 0, 'spam': 0}