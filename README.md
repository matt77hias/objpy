[![License][s1]][li]

[s1]: https://img.shields.io/badge/licence-GPL%203.0-blue.svg
[li]: https://raw.githubusercontent.com/matt77hias/objpy/master/LICENSE.txt

# objpy

## About
* `obj_parser.py`: A lightweight Wavefront OBJ parser which only supports vertices and faces.
* `obj_converter.py`: A Wavefront OBJ to Wavefront OBJ Converter which centers models at (Origin.x, Min.y, Origin.z) and isotropically rescales models to [0,1]^3.

## Use
```python
import obj_parser

vertices, faces = obj_parser.parse(fname)
```
