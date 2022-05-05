#!/usr/local/bin/python3

from model.gate import Identity

def print_list(elements):
        res = ""
        
        for element in elements:
            res += str(element) + "\t"
        
        print(res[: -1])
