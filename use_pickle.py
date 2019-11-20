# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 11:41:41 2019

@author: rpothams
"""

import pickle

file = open('function_network', 'rb')
fun_network = pickle.load(file)

if __name__ == "__main__":

    for i in range(1):
        input_func = input("Enter input function: ")
        input_func = str(input_func)

        if input_func == 'exit':
            print('program exitted')
            break
        elif fun_network.validate_user_input(input_func):
            print(fun_network.get_affected_functions(input_func, 'bfs'))
            print('------------------------------------------')
            print(fun_network.get_affected_functions(input_func, 'dfs'))
            print('------------------------------------------')
            print(fun_network.get_affected_functions(input_func, 'topo'))
