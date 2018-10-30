# -*- coding: utf-8 -*-

'''
A Wavefront OBJ normalizer.
@author     Matthias Moulin
@version    2.0
'''

import re
from decimal import Decimal, getcontext

getcontext().prec = 23

REGEX_FLOAT = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
rx = re.compile(REGEX_FLOAT, re.VERBOSE)

def get_floats(string):
    return list(map(float, rx.findall(string)))

class Normalizer(object):

    def __init__(self, name):
        self.__name__ = name
        self.m_min = [Decimal( 100000), Decimal( 100000), Decimal( 100000)]
        self.m_max = [Decimal(-100000), Decimal(-100000), Decimal(-100000)]

    def add(self, vertex_coordinates):
        vertex     = list(map(Decimal, vertex_coordinates))
        self.m_min = list(map(min, zip(self.m_min, vertex)))
        self.m_max = list(map(max, zip(self.m_max, vertex)))

    def finish(self):
        self.m_c =     list(map(lambda x: (x[1] + x[0]) / 2, zip(self.m_min, self.m_max)))
        self.m_d = max(list(map(lambda x:  x[1] - x[0],      zip(self.m_min, self.m_max))))

    def normalize(self, vertex_coordinates):
        vertex = list(map(Decimal, vertex_coordinates))
        return list(map(lambda x: float((x[1] - x[0]) / self.m_d), zip(self.m_c, vertex)))

    def __repr__(self):
        return self.__name__ \
                + ' {0} {1} {2} 0 0 0'.format(*list(map(float, self.m_c))) \
                + ' {0} {0} {0}'.format(float(self.m_d))

    def __str__(self):
        return self.__name__ \
                + '\nBefore:' \
                + '\nMin: {0} {1} {2}'.format(*list(map(float, self.m_min))) \
                + '\nMax: {0} {1} {2}'.format(*list(map(float, self.m_max))) \
                + '\nAfter:' \
                + '\nC: {0} {1} {2}'.format(*list(map(float, self.m_c))) \
                + '\nD: {0}'.format(float(self.m_d))

def convert(fname):

    # Calculate the normalization values to center the scene at its centroid 
    # and unfirmorly rescale the scene to [0,1]^3 
    current = Normalizer('scene')
    with open(fname, 'r') as fin:
        for line in fin:   
            
            if line.startswith('v '):
                current.add(get_floats(line))
    
    current.finish()
    print(current)
    print()

    # Normalize the scene
    with open(fname + '1', 'w') as fout:
        with open(fname, 'r') as fin:
            for line in fin:
                
                if line.startswith('v '):
                    floats = current.normalize(get_floats(line))
                    fout.write('v {0} {1} {2}\n'.format(floats[0], floats[1], floats[2]))
                    continue
                
                if line.startswith('vt'):
                    floats = get_floats(line)
                    fout.write('vt {0} {1}\n'.format(floats[0], floats[1]))
                    continue
                
                fout.write(line)

    # Calculate the normalization values to center each group at its centroid 
    # and unfirmorly rescale each group to [0,1]^3 
    ns_group = {} 
    current  = None
    with open(fname + '1', 'r') as fin:
        for line in fin:   
            
            if line.startswith('g'):
                
                if (current is not None):
                    current.finish()
                    print(current)
                    print()
                
                name = line.split(' ')[1][:-1]
                current = Normalizer(name)
                ns_group[name] = current
                continue

            if line.startswith('v ') and current is not None:
                current.add(get_floats(line))
                continue

    if (current is not None):
       current.finish()
       print(current)
       print()
    else:
        return

    # Normalize the scene
    current  = None
    with open(fname + '2', 'w') as fout:
        with open(fname + '1', 'r') as fin:
            for line in fin:
                
                if line.startswith('g'):
                    name = line.split(' ')[1][:-1]
                    current = ns_group[name]
                    fout.write('g ' + current.__repr__() + '\n')
                    continue
                
                if line.startswith('v '):
                    floats = current.normalize(get_floats(line))
                    fout.write('v {0} {1} {2}\n'.format(floats[0], floats[1], floats[2]))
                    continue
                
                fout.write(line)
