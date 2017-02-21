#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import networkx as nx
from datetime import datetime

g = nx.Graph()
g.add_node("John",{'name': 'John','age': 25})
g.add_node("Peter",{'name': 'Peter','age': 35})
g.add_node("Mary",{'name': 'Mary','age': 31})
g.add_node("Lucy",{'name': 'Lucy','age': 19})
g.add_edge("John","Mary", {'since':datetime.today()})
g.add_edge("John","Peter", {'since':datetime(1990, 7,30)})
g.add_edge("Mary","Lucy", {'since':datetime(2010, 8,10)})

print(g.nodes())
print(g.edges())
print(g.has_edge("Lucy", "Mary"))