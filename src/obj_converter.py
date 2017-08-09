# -*- coding: utf-8 -*-

'''
A Wavefront OBJ to Wavefront OBJ Converter which
* centers models at (Origin.x, Min.y, Origin.z)
* isotropically rescales models to [0,1]^3
@author     Matthias Moulin
@version    1.0
'''

import re
from decimal import Decimal, getcontext

REGEX_FLOAT = '[+-]?[0-9.]+'

def get_normalization_values(fname_in): 
    getcontext().prec = 23
    
    min_x = Decimal(100000)
    min_y = Decimal(100000)
    min_z = Decimal(100000)
    max_x = Decimal(-100000)
    max_y = Decimal(-100000)
    max_z = Decimal(-100000)

    with open(fname_in, 'r') as fin:
        for line in fin:   
            if line.startswith('v '):
                floats = get_floats(line)
                
                x = Decimal(floats[0])
                y = Decimal(floats[1])
                z = Decimal(floats[2])
                
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                min_z = min(min_z, z)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
                max_z = max(max_z, z)

    cx = (min_x + max_x) / 2
    cy = min_y
    cz = (min_z + max_z) / 2
       
    dx = max_x - min_x
    dy = max_y - min_y
    dz = max_z - min_z
    d = max(dx, dy, dz)
    
    print('Before:')
    print('Min: {0} {1} {2}'.format(float(min_x), float(min_y), float(min_z)))
    print('Max: {0} {1} {2}'.format(float(max_x), float(max_y), float(max_z)))
    print('After:')
    print('C: {0} {1} {2}'.format(float(cx), float(cy), float(cz)))
    print('D: {0}'.format(float(d)))
    
    return cx, cy, cz, d

def get_floats(string):
    return map(float, re.findall(REGEX_FLOAT, string))
def get_float2(string):
    floats = get_floats(string)
    x = floats[0]
    y = floats[1]
    return '{0} {1}'.format(x, y)
def get_float3(string):
    floats = get_floats(string)
    x = floats[0]
    y = floats[1]
    z = floats[2]
    return '{0} {1} {2}'.format(x, y, z)
def get_normalized_float3(string, cx, cy, cz, d):
    floats = get_floats(string)
    x = float((Decimal(floats[0]) - cx) / d)
    y = float((Decimal(floats[1]) - cy) / d)
    z = float((Decimal(floats[2]) - cz) / d)
    return '{0} {1} {2}'.format(x, y, z)

def convert(fname_in, fname_out, material=False):
    cx, cy, cz, d = get_normalization_values(fname_in)

    with open(fname_out, 'w') as fout:
        with open(fname_in, 'r') as fin:
            for line in fin:
                
                if line.startswith('vt'):
                    fout.write('vt ' + get_float2(line) + '\n')
                    continue
                if line.startswith('vn'):
                    fout.write('vn ' + get_float3(line) + '\n')
                    continue
                if line.startswith('v'):
                    fout.write('v ' + get_normalized_float3(line, cx, cy, cz, d) + '\n')
                    continue
                if line.startswith('f'):
                    fout.write(line)
                    continue
                if material:
                    if line.startswith('g') \
                    or line.startswith('mtllib') \
                    or line.startswith('usemtl'):
                        fout.write(line)
