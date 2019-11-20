# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 11:41:41 2019

@author: rpothams
"""
import re
from collections import defaultdict, deque

class FunctionNetwork:
    '''Class to parse function mapping doc and build a directed graph
    '''

    def __init__(self):
        '''Initiate a dictionary for function mapping
        '''
        self.graph = defaultdict(list)

    def addVertex(self, u):
        '''Add a function to the FunctionNetwork

        Keyword arguments:
        u -- function
        output -- Boolean(True - if vertex added else False)
        '''
        if u[0] != '$':
            return False

        if u not in self.graph:
            self.graph[u]

        return True

    def addEdge(self, u, v):
        '''Add chile to parent directed map

        Keyword arguments:
        u  -- child function
        v -- parent function
        output -- Boolean (True - if edge created else False)
        '''
        if u[0] != '$':
            return False

        self.graph[u].append(v)

        return True

    def create_function_map(self, function_df, parent_col, child_col):
        '''Create a directed graph from the functions mapping input

        Keyword arguments:
        function_df -- dataframe with parent and child function mapping
        parent_col -- column name of parent functions
        child_col -- column name of child functions
        '''
        try:
            function_df.apply(self.util_func_parser, args= (parent_col, child_col, r'\$\w+'), axis = 1)
        except Exception:
            print('Parsing Failed... :(')

    def util_func_parser(self, row, parent_col, child_col, pattern):
        '''Utility function that parses each mapping and adds to the FunctionNetwork
        Finds all functions that start with '$' and contains only alphanumeric charactes including '_'
        '''
        child_funcs = re.findall(pattern, row[child_col])
        child_funcs = list(dict.fromkeys(child_funcs))
        parent_func = row[parent_col]

        for i in range(len(child_funcs)):
            if not self.addVertex(parent_func):
                print('Invalid parent function in the input (probable parsing fail): {}'.format(parent_func))
                continue
            if not self.addEdge(child_funcs[i], parent_func):
                print("Invalid child function in the input (probable parsing fail): {}".format(child_funcs[i]))

        return row

    def get_affected_functions(self, search_node, algo = 'bfs'):
        '''Finds all functions affected by changes in the given input function name
        '''
        if algo == 'dfs':
            return self.get_affected_functions_depth(search_node, {}, 0)
        elif algo == 'bfs':
            return self.get_affected_functions_bfs(search_node)
        else:
            # Use topological sort
            return self.get_affected_functions_toposort(search_node, set(), [])

    def get_affected_functions_depth(self, search_node, visited_nodes, level = 0):
        ''' Find all affected functions using depth first search

        Keyword arguments:
        search_node -- input function
        '''
        all_parent_nodes = self.graph[search_node]
        visited_nodes[search_node] = level

        if len(all_parent_nodes) == 0:
            return visited_nodes

        level += 1
        for node in all_parent_nodes:
            if node not in visited_nodes:
                self.get_affected_functions_depth(node, visited_nodes, level)

        return visited_nodes

    def get_affected_functions_bfs(self, search_node):
        '''Find all affected functions using BFS

        Keyword arguments:
        search_node -- input function
        '''
        queue = deque()
        queue.append(search_node)
        level = 0
        visited_nodes = {}
        visited_nodes[search_node] = level

        while queue:
            queue_size = len(queue)

            for i in range(queue_size):
                func = queue.popleft() #pop the right most
                queue.extend(self.graph[func] - visited_nodes.keys())
                visited_nodes[func] = level
            level += 1

        return visited_nodes

    def get_affected_functions_toposort(self, search_node, visited_nodes, stack):
        '''Find all affected functions using topological sorting order
        '''
        visited_nodes.add(search_node)

        for node in self.graph[search_node]:
            if node not in visited_nodes:
                self.get_affected_functions_toposort(node, visited_nodes, stack)

        stack.insert(0, search_node)

        return stack

    def validate_user_input(self, func):
        '''checks whether the user input is valid
        '''
        if func not in self.graph:
            print("Not a known function, verify input func")
            return False
        else:
            return True
