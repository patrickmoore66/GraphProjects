# Course: CS261
# Author: Patrick Moore
# Assignment: 6
# Description: Undirected and Directed Graphs


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        self.adj_list[v] = []
        return

        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return
        elif self.adj_list.get(u) == None:
            self.adj_list.setdefault(u, [v])
            if self.adj_list.get(v) == None:
                self.adj_list.setdefault(v, [u])
                return
            else:
                if u not in self.adj_list[v]:
                    self.adj_list[v].append(u)
                    return
                else:
                    return
        else:
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)
                if self.adj_list.get(v) == None:
                    self.adj_list.setdefault(v, [u])
                else:
                    if u not in self.adj_list[v]:
                        self.adj_list[v].append(u)
                        return
                    else:
                        return
            else:
                if self.adj_list.get(v) == None:
                    self.adj_list.setdefault(v, [u])
                    return
                else:
                    if u not in self.adj_list[v]:
                        self.adj_list[v].append(u)
                        return
                    else:
                        return


    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if self.adj_list.get(v) == None or self.adj_list.get(u) == None:
            return
        elif u not in self.adj_list[v] or v not in self.adj_list[u]:
            return
        else:
            self.adj_list[v].remove(u)
            self.adj_list[u].remove(v)
            return

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if self.adj_list.get(v) != None:
            self.adj_list.pop(v)
            for key in self.adj_list:
                if v in self.adj_list[key]:
                    self.adj_list[key].remove(v)
            return
        

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        result = []
        for key in self.adj_list:
            result.append(key)

        return result
       

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        result = []
        for key in self.adj_list:
            for edge in self.adj_list[key]:
                if (edge, key) not in result:
                    result.append((key, edge))
        return result

        

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        i = 0
        length = len(path) - 1
        while i < length:
            cur = path[i]
            next = path[i+1]
            if path[i+1] not in self.adj_list[path[i]]:
                return False
            i+=1
        vertices = self.get_vertices()
        if length == 0 and path[0] not in vertices:
            return False
        return True
       

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        result = []
        stack = []

        stack.append(v_start)
        cur = stack.pop()
        vertices = self.get_vertices()
        if v_start not in vertices:
            return result
        while len(stack) >= 0:
            if cur not in result:
                result.append(cur)
                temp = self.adj_list[cur]
                temp.sort()
                temp.reverse()
                for edge in temp:
                    stack.append(edge)

            if cur == v_end:
                return result
            if len(stack) == 0:
                break
            else:
                cur = stack.pop()

        return result



    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        result = []
        que = []

        que.insert(0, v_start)
        cur = que.pop()
        vertices = self.get_vertices()
        if v_start not in vertices:
            return result
        while len(que) >= 0:
            if cur not in result:
                result.append(cur)
                temp = self.adj_list[cur]
                temp.sort()
                for edge in temp:
                    que.insert(0,edge)

            if cur == v_end:
                return result
            if len(que) == 0:
                break
            else:
                cur = que.pop()

        return result
        

    def count_connected_components(self) -> int:
        """
        Return number of connected components in the graph
        """
        graph = self.get_vertices()
        count = 0

        while graph != []:
            for vertex in graph:
                connected = self.dfs(vertex)
                for edge in connected:
                    if edge in graph:
                        graph.remove(edge)
                count+=1

        return count


    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
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
            for edge in self.adj_list[cur]:
                if edge in visited and edge in vertices:
                    if edge == cur or edge != parent:
                        return True
                elif edge in vertices and self.has_cycle_helper(edge, cur, visited, vertices, stack, index):
                    return True
            if len(vertices) > 1:
                vertices.remove(cur)
                visited.clear()
                if self.has_cycle_helper(vertices[0], None, visited, vertices, stack, index):
                    return True
            return False


   


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
