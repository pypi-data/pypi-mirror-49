class Graph(object):
    '''
        graph in the form
        {
            node = [[nodeA, weigh1], [nodeB, weigh2]],
            nodeA = [[nodeC, weigh3]]
        }
    '''
    def __init__(self):
        self.graph = {}

    def __init__(self, graph):
        self.graph = graph

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, node_start, node_end, weight):
        edges = self.graph[node_start]
        for item in edges:
            if item[0] == node_end:
                raise ValueError("Edge already exiists")

        self.graph[node_start].append([weight, node_end])

    def delete_node(self, node):
        self.graph.pop(node, None)

    def delete_edge(self, node_start, node_end):
        edges = self.graph[node_start]
        for item in edges:
            if item[0] == node_end:
                self.graph[node_start].remove(item)

    def get_node_details(self, node):
        if node in self.graph:
            return self.graph[node]
