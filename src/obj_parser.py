# -*- coding: utf-8 -*-

'''
A lightweight Wavefront OBJ parser which only supports vertices and faces.
@author     Matthias Moulin
@version    1.0
'''

import numpy as np

TOKEN_COMMENT = '#'
TOKEN_VERTEX = 'v'
TOKEN_FACE = 'f'

print_unsupported = False

def parse(fname):
    line_nb = 0
    vertices = []
    faces = []
    with open(fname, 'r') as infile:
        for line in infile:
            line_nb += 1
            if line.startswith(TOKEN_COMMENT):
                continue
            parts = line.split()
            nb_parts = len(parts)
            if nb_parts == 0:
                continue
            if parts[0] == TOKEN_VERTEX and nb_parts > 1:
                vertices.append(parse_vertex(parts[1:]))
            elif parts[0] == TOKEN_FACE and nb_parts > 1:
                faces.append(parse_face(parts[1:]))
            elif print_unsupported:
                print('Line {0}:  Not supported'.format(line_nb))
    return vertices, faces
                
def parse_vertex(parts):
    return np.array(map(np.float64, parts))
    
def parse_face(parts):
    return np.array([parse_face_vertex(part) for part in parts])
    
def parse_face_vertex(part):
    if '//' in part:
        return np.int64(part.split('//')[0]) - 1
    elif '/' in part:
        return np.int64(part.split('/')[0]) - 1
    else:
        return np.int64(part) - 1
