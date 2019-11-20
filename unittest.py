#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 23:50:31 2019

@author: rajeshpothamsetty
"""
import unittest
from create_graph_v4 import FunctionNetwork

class TestFunctionNetwork(unittest.TestCase):

    def test_addVertex(self):
        '''
        Test: check if addVertex has no issue adding a valid function
        '''
        result = FunctionNetwork().addVertex('$testfunc')
        self.assertEqual(result, True)

    def test_addVertex2(self):
        '''
        Test: check if any parent function with no '$' as prefix is added to the function map.
        '''
        result = FunctionNetwork().addVertex('funcwithNo$')
        self.assertEqual(result, False)


    def test_addEdge(self):
        '''
        Test: check if invalid child function is not added.
        '''
        result = FunctionNetwork().addEdge('xx', '$yy')
        self.assertEqual(result, False)

    def test_valid_user_input(self):
        '''
        Test: check if valid_user_input works as expected
        '''
        result = FunctionNetwork().validate_user_input('$yy')
        self.assertEqual(result, False)

    def test_get_affected_functions(self):
        '''
        Test: check if given condition in the problem statement is satisfied
        '''
        g = FunctionNetwork()
        g.addVertex('$rssec6')
        g.addEdge('$rssec5', '$rssec6')
        g.addEdge('$rssec6', '$gstmom1')

        result = g.get_affected_functions('$rssec5', 'dfs')
        
        if '$rssec6' in result.keys() and '$gstmom1' in result.keys():
            match = True
        
        self.assertEqual(match, True)

    def test_parse_function_list(self):
        '''
        Test: check whether valid functions with '_' in the function name.
        '''
        def compose():
            pass


if __name__ == '__main__':
    unittest.main()
