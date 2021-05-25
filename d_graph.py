# Course: CS261
# Author: Patrick Moore
# Assignment: 6
# Description: Undirected and Directed Graphs

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a new vertex to the graph. Vertex name does not need to be provided, instead vertex
        is assigned a reference index (integer). First vertex created in the graph is assigned
        index 0, subsequent vertices have indexes 1, 2, 3 etc. This ​method returns a single integer
        the number of vertices in the graph after the addition.
        """
        if self.v_count == 0:
            self.adj_matrix.append([0])
            self.v_count+=1
        else:
            i = 1
            for element in self.adj_matrix:
                element.append(0)
                i+=1
            temp = [0] * i
            self.adj_matrix.append(temp)
            self.v_count+=1

        return self.v_count


    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds a new edge to the graph, connecting two vertices with provided indices. If either
        (or both) vertex indices do not exist in the graph, or if the ​weight​ is not a positive
        integer, or if ​src​ and ​dst​ refer to the same vertex, the method does nothing. If an edge
        already exists in the graph, the method updates its weight.
        """
        if src >= len(self.adj_matrix) or src < 0:
            return
        elif dst >= len(self.adj_matrix[src]) or dst < 0:
            return
        elif weight < 1:
            return
        elif src == dst:
            return
        else:
            self.adj_matrix[src][dst] = weight
            return


    def remove_edge(self, src: int, dst: int) -> None:
        """
        This method removes an edge between two vertices with provided indices. If either (or both)
        vertex indices do not exist in the graph, or if there is no edge between them, the method
        does nothing.
        """
        if src >= len(self.adj_matrix) or src < 0:
            return
        elif dst >= len(self.adj_matrix[src]) or dst < 0:
            return
        elif self.adj_matrix[src][dst] == 0:
            return
        else:
            self.adj_matrix[src][dst] = 0
            return

    def get_vertices(self) -> []:
        """
        Returns a list of vertices of the graph.
        """
        result = []
        i = 0
        for vertex in self.adj_matrix:
            result.append(i)
            i+=1
        return result

    def get_edges(self) -> []:
        """
        Returns a list of edges in the graph. Each edge is returned as a tuple of two incident
        vertex indices and weight. First element in the tuple refers to the source vertex. Second
        element in the tuple refers to the destination vertex. Third element in the tuple is the
        weight of the edge.
        """
        result = []
        i = 0
        j = 0

        while i < len(self.adj_matrix):
            while j < len(self.adj_matrix[i]):
                test = self.adj_matrix[i][j]
                if self.adj_matrix[i][j] != 0:
                    result.append((i,j, self.adj_matrix[i][j]))
                    j+=1
                else:
                    j+=1
            j = 0
            i+=1

        return result

    def is_valid_path(self, path: []) -> bool:
        """
        Takes a list of vertex indices and returns True if the sequence of vertices represents a
        valid path in the graph (so one can travel from the first vertex in the list to the last
        vertex in the list, at each step traversing over an edge in the graph). Empty path is
        considered valid.
        """
        if path == []:
            return True
        else:
            i = 0
            while i < (len(path)-1):
                if path[i] < 0 or path[i] >= len(self.adj_matrix):
                    return False
                else:
                    if self.adj_matrix[path[i]][path[i+1]] == 0:
                        return False
                    else:i+=1
            return True


    def dfs(self, v_start, v_end=None) -> []:
        """
        Performs a depth-first search (DFS) in the graph and returns a list of vertices
        visited during the search, in the order they were visited. It takes one required parameter,
        index of the vertex from which the search will start, and one optional parameter - index of
        the ‘end’ vertex that will stop the search once that vertex is reached.
        """
        result = []
        stack = []


        stack.append(v_start)

        if v_start >= len(self.adj_matrix) or v_start < 0:
            return result

        while stack != []:
            cur = stack.pop()
            if cur not in result:
                result.append(cur)
                i = 0
                temp = []
                while i < len(self.adj_matrix[cur]):
                    if self.adj_matrix[cur][i] != 0:
                        temp.append(i)
                    i+=1
                temp.sort()
                while temp != []:
                    stack.append(temp.pop())

        return result




    def bfs(self, v_start, v_end=None) -> []:
        """
        Same as DFS, but performs Breadth-First-Search
        """
        result = []
        que = []

        que.insert(0,v_start)

        if v_start >= len(self.adj_matrix) or v_start < 0:
            return result

        while que != []:
            cur = que.pop()
            if cur not in result:
                result.append(cur)
                i = 0
                temp = []
                while i < len(self.adj_matrix[cur]):
                    if self.adj_matrix[cur][i] != 0:
                        que.insert(0,i)
                    i += 1

        return result

    def has_cycle(self):
        """
        Returns True if there is at least one cycle in the graph. If the graph is acyclic, the method
        returns False
        """
        vertices = self.get_vertices()

        if len(vertices) <= 2:
            return False
        else:
            index = 0
            visited = []
            stack = []
            parent = None
            cur = vertices[0]
            return self.has_cycle_helper(cur, parent, visited, vertices, stack, index)

    def has_cycle_helper(self, cur, parent, visited, vertices, stack, index):
        visited.append(cur)

        i = 0
        while i < len(self.adj_matrix[cur]):
            if self.adj_matrix[cur][i] != 0:
                edge = self.adj_matrix[cur][i]
                if i in visited and i in vertices:
                    if i == cur or i != parent:
                        return True
                    elif self.adj_matrix[i][cur]!=0:
                        return True
                elif i in vertices and self.has_cycle_helper(i, cur, visited, vertices, stack, index):
                    return True
            i+=1
        if len(vertices) > 1:
            vertices.remove(cur)
            visited.clear()
            if self.has_cycle_helper(vertices[0], None, visited, vertices, stack, index):
                return True
        return False


        return True



    def dijkstra(self, src: int) -> []:
        """
        Implements the Dijkstra algorithm to compute the length of the shortest path from a given
        vertex to all other vertices in the graph. It returns a list with one value per each vertex
        in the graph, where value at index 0 is the length of the shortest path from vertex SRC to
        vertex 0, value at index 1 is the length of the shortest path from vertex SRC to vertex 1
        etc. If a certain vertex is not reachable from SRC, returned value is INFINITY (float(‘inf’)).
        """
        visited = [(float('inf'))] * self.v_count
        pqueue = []

        #lists in python sort tuples by the first element,so distance will always be first with node second
        pqueue.insert(0, (0, src))
        prev = None

        while pqueue != []:
            temp = pqueue.pop(0)#add index 0
            v = temp[1]
            d = temp[0]

            if visited[v] == (float('inf')):
                visited[v] = d

                i = 0
                while i < len(self.adj_matrix[v]):
                    if self.adj_matrix[v][i] != 0:
                        d_neighbor = self.adj_matrix[v][i]
                        d_neighbor += d


                        pqueue.insert(0, (d_neighbor,i))
                        pqueue.sort()

                    i+=1
            if visited[v] > d:
                visited[v] = d

        return visited







if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - method has_cycle() example 2")
    print("----------------------------------")
    edges = [(2,1,17), (2,3,9), (3,5,1), (3,2,10), (4,0,12), ]
    g = DirectedGraph(edges)
    print(g)

    print(g.get_edges(), g.has_cycle(), sep='\n')



    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
