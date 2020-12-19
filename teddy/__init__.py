"""

teddy - A utilities library for my python projects

=======
Methods
=======
get_length_itertools(iter_type, iter_obj, iter_size)
    Returns the total number of iterable items.

"""
from math import factorial as mf
import sys
import os
# import markdown

def binomail(n, r):
    return (mf(n)/(mf(r)*mf(n-r)))

def split_string(line, n):
    return [line[i:i+n] for i in range(0, len(line), n)]

def xor2(s1, s2):
    c_max = max(s1, s2)
    c_min = min(s1, s2)
    i_min = 0
    r = ''
    for i_max in range(len(c_max)):
        if i_min  == len(c_min):
            i_min = 0
        r += chr(ord(c_min[i_min])^ord(c_max[i_max]))
        i_min += 1
    return r

def get_length_itertools(iter_type, iter_obj, iter_size):
    """
    Python's itertools module provides many utilities for handling iterable objects.
    However, it lacks the ability to provide a total number of items in an object.
    This method will return the total number of iterable items in an object.

    ==========
    Parameters
    ==========
    iter_type : str
        The type of itertools iterable object.
        ==============    ===============================================
        iter_type         example elements (iter_size = 2)
        ==============    ===============================================
        'combinations'    AB AC AD BC BD CD
        'permutations'    AB AC AD BA BC BD CA CB CD DA DB DC
        'product'         AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
        ==============    ===============================================
    iter_obj : str, list
        The object containing all possible items for itertools to populate.
    iter_size : int
        The number of elements in the subsequence of iterable object.

    =======
    Returns
    =======
    total : int
        The total number of subsequence iterable objects
    """

    candidates = len(iter_obj)
    if 'permutation' in iter_type:
        total = 1
        for i in range(iter_size):
            total *= (candidates - i)
    elif 'product' in iter_type:
        total = candidates ** iter_size
    elif 'combination' in iter_type:
        total = binomail(candidates, iter_size)
    return total


def js_minify(raw):
    modifiers = ['\n', '\t', '    ', '  ']
    for m in modifiers:
        raw = raw.replace(m, '')
    return raw.replace(' = ','=').replace(') {','){').replace(', ',',')


def find_cmd(cmd, find_all=False):
    cmds = []
    for cmd_path in os.environ['PATH'].split(':'):
        if os.path.isdir(cmd_path) and cmd in os.listdir(cmd_path):
            bin_cmd = os.path.join(cmd_path, cmd)
            if find_all:
                cmds += [bin_cmd]
            else:
                return bin_cmd
    return cmds


if __name__ == '__main__':
    option = sys.argv[1:]
    if option == 'emacs':
        print('')
