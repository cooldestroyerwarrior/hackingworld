import matplotlib.pyplot as plt
import networkx as nx
#node
g=nx.Graph()
g.add_edge(1,2)
g.add_edge(1,4)
g.add_edge(1,5)
g.add_edge(2,3)
g.add_edge(3,8)
g.add_edge(3,4)
g.add_edge(4,1)
g.add_edge(4,8)
g.add_edge(8,3)
g.add_edge(8,4)
g.add_edge(5,7)
g.add_edge(5,6)

node_list=g.nodes()
print("Nodes:", node_list)
edge_list=g.edges()
print("Edges:", edge_list)
n=g.number_of_nodes()
print("total number of nodes.",n)
m=g.number_of_edges()
print("Total edges in the graph are ", m)
# Use the degree method to get in-degrees and out-degrees
degrees = dict(g.degree())

print("Degree for all the nodes:", degrees)
# Print the successors of node 2
z=list(g.neighbors(2))
print("neighbors of Node 2 is :", z)




nx.draw(g,with_labels=True)
plt.show()
