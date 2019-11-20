# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 11:41:41 2019

@author: rpothams
"""

import pandas as pd
from create_graph_v4 import FunctionNetwork
import pickle

if __name__ == "__main__":

    func_df = pd.read_csv('func_parsed.csv', header = 0) #verify file loaded as expected
    parent_col = func_df.columns[0]
    child_col = func_df.columns[1]

    g = FunctionNetwork()
    g.create_function_map(func_df, parent_col, child_col)

    #save the function mapping for later use
    file = open('function_network', 'wb')
    pickle.dump(g, file)

    for i in range(1):
        input_func = input("Enter input function: ")
        input_func = str(input_func)

        if input_func == 'exit':
            print('program exitted')
            break
        elif g.validate_user_input(input_func):
            print(g.get_affected_functions(input_func, 'bfs'))
            print('------------------------------------------')
            print(g.get_affected_functions(input_func, 'dfs'))
            print('------------------------------------------')
            print(g.get_affected_functions(input_func, 'topo'))
            #print(g.get_affected_functions(input_func, {}))
