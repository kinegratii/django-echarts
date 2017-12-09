# coding=utf8

from __future__ import unicode_literals

import networkx as nx
from networkx.readwrite import json_graph
from pyecharts import Graph

g = nx.Graph()
categories = ['网关', '节点']
g.add_node('FF12C904', name='Gateway 1', symbolSize=40, category=0)
g.add_node('FF12CA02', name='Node 11', category=1)
g.add_node('FF12C326', name='Node 12', category=1)
g.add_node('FF45C023', name='Node 111', category=1)
g.add_node('FF230933', name='Node 1111', category=1)

g.add_edge('FF12C904', 'FF12CA02')
g.add_edge('FF12C904', 'FF12C326')
g.add_edge('FF12CA02', 'FF45C023')
g.add_edge('FF45C023', 'FF230933')

g_data = json_graph.node_link_data(g)
print(g_data)
eg = Graph('设备最新拓扑图')
eg.add('Devices', nodes=g_data['nodes'], links=g_data['links'], categories=categories)
# eg.show_config()
eg.render()
