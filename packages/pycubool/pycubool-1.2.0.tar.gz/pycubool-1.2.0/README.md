![Project logo](https://github.com/JetBrains-Research/cuBool/blob/master/docs/logo/cubool_logo_trsp.png?raw=true)

# pycubool

[![JB Research](https://jb.gg/badges/research-flat-square.svg)](https://research.jetbrains.org/)
[![Ubuntu](https://github.com/JetBrains-Research/cuBool/workflows/Ubuntu/badge.svg?branch=master)](https://github.com/JetBrains-Research/cuBool/actions)
[![License](https://img.shields.io/badge/license-MIT-orange)](https://github.com/JetBrains-Research/cuBool/blob/master/LICENSE)

**pycubool** is a python wrapper for [cuBool](https://github.com/JetBrains-Research/cuBool) library.

**cuBool** is a linear Boolean algebra library primitives and operations for 
work with sparse matrices written on the NVIDIA CUDA platform. The primary 
goal of the library is implementation, testing and profiling algorithms for
solving *formal-language-constrained problems*, such as *context-free* 
and *regular* path queries with various semantics for graph databases.
The library provides C-compatible API, written in the GraphBLAS style.

**The library** is shipped with python package **pycubool** - wrapper for
cuBool library C API. This package exports library features and primitives 
in high-level format with automated resources management and fancy syntax sugar.

**The primary library primitives** are sparse matrix and sparse vector of boolean values. 
The library provides the most popular operations for matrix manipulation, 
such as construction from values, transpose, sub-matrix/sub-vector extraction, matrix-to-vector reduce, 
element-wise addition, matrix-matrix, matrix-vector, vector-matrix multiplication, and Kronecker product.  

**As a fallback** library provides sequential backend for mentioned above operations
for computations on CPU side only. This backend is selected automatically
if Cuda compatible device is not presented in the system. This can be quite handy for 
prototyping algorithms on a local computer for later running on a powerful server.   

### Features

- Cuda backend for computations
- Cpu backend for computations
- Matrix/vector creation (empty, from data, with random data)
- Matrix-matrix operations (multiplication, element-wise addition, kronecker product)
- Matrix-vector operations (matrix-vector and vector-matrix multiplication)
- Vector-vector operations (element-wise addition)
- Matrix operations (equality, transpose, reduce to vector, extract sub-matrix)
- Vector operations (equality, reduce to value, extract sub-vector)
- Matrix/vector data extraction (as lists, as list of pairs)
- Matrix/vector syntax sugar (pretty string printing, slicing, iterating through non-zero values)
- IO (import/export matrix from/to `.mtx` file format)
- GraphViz (export single matrix or set of matrices as a graph with custom color and label settings)
- Debug (matrix string debug markers, logging)

### Performance

Sparse Boolean matrix-matrix multiplication evaluation results are listed bellow.
Machine configuration: PC with Ubuntu 20.04, Intel Core i7-6700 3.40GHz CPU, DDR4 64Gb RAM, GeForce GTX 1070 GPU with 8Gb VRAM. 

![time](https://github.com/JetBrains-Research/cuBool/raw/master/docs/pictures/mxm-perf-time.svg?raw=true&sanitize=true)
![mem](https://github.com/JetBrains-Research/cuBool/raw/master/docs/pictures/mxm-perf-mem.svg?raw=true&sanitize=true)

The matrix data is selected from the SuiteSparse Matrix Collection [link](https://sparse.tamu.edu).

| Matrix name              | # Rows      | Nnz M       | Nnz/row   | Max Nnz/row | Nnz M^2     |
|---                       |---:         |---:         |---:       |---:         |---:         |
| SNAP/amazon0312          | 400,727     | 3,200,440   | 7.9       | 10          | 14,390,544  |
| LAW/amazon-2008          | 735,323     | 5,158,388   | 7.0       | 10          | 25,366,745  |
| SNAP/web-Google          | 916,428     | 5,105,039   | 5.5       | 456         | 29,710,164  |
| SNAP/roadNet-PA          | 1,090,920   | 3,083,796   | 2.8       | 9           | 7,238,920   |
| SNAP/roadNet-TX	       | 1,393,383   | 3,843,320   | 2.7       | 12          | 8,903,897   |
| SNAP/roadNet-CA	       | 1,971,281   | 5,533,214   | 2.8       | 12          | 12,908,450  |
| DIMACS10/netherlands_osm | 2,216,688   | 4,882,476   | 2.2       | 7           | 8,755,758   |
  
Detailed comparison is available in the full paper text at 
[link](https://github.com/YaccConstructor/articles/blob/master/2021/GRAPL/Sparse_Boolean_Algebra_on_GPGPU/Sparse_Boolean_Algebra_on_GPGPU.pdf).

### Simple example

Create sparse matrices, compute matrix-matrix product and print the result to the output:

```python
import pycubool as cb

a = cb.Matrix.empty(shape=(2, 3))
a[0, 0] = True
a[1, 2] = True

b = cb.Matrix.empty(shape=(3, 4))
b[0, 1] = True
b[0, 2] = True
b[1, 3] = True
b[2, 1] = True

print(a, b, a.mxm(b), sep="\n")
```

### Vector example

Create sparse matrix and vector, compute matrix-vector and vector-matrix products and print the result:

```python
import pycubool as cb

m = cb.Matrix.empty(shape=(3, 4))
m[0, 1] = True
m[1, 0] = True
m[1, 3] = True
m[2, 2] = True

v = cb.Vector.empty(nrows=4)
v[0] = True
v[2] = True

t = cb.Vector.empty(nrows=3) 
t[0] = True
t[2] = True

print(m.mxv(v), t.vxm(m), sep="\n")
```

### Transitive closure example

Compute the transitive closure problem for the directed graph and print the result:

```python
import pycubool as cb

a = cb.Matrix.empty(shape=(4, 4))
a[0, 1] = True
a[1, 2] = True
a[2, 0] = True
a[2, 3] = True
a[3, 2] = True

t = a.dup()                             # Duplicate matrix where to store result
total = 0                               # Current number of values

while total != t.nvals:
    total = t.nvals
    t.mxm(t, out=t, accumulate=True)    # t += t * t

print(a, t, sep="\n")
```

### GraphViz example

Generate GraphViz graph script for a graph stored as a set of adjacency matrices:

```python
import pycubool as cb

name = "Test"                           # Displayed graph name   
shape = (4, 4)                          # Adjacency matrices shape
colors = {"a": "red", "b": "green"}     # Colors per label

a = cb.Matrix.empty(shape=shape)        # Edges labeled as 'a'
a[0, 1] = True
a[1, 2] = True
a[2, 0] = True

b = cb.Matrix.empty(shape=shape)        # Edges labeled as 'b'
b[2, 3] = True
b[3, 2] = True

print(cb.matrices_to_gviz(matrices={"a": a, "b": b}, graph_name=name, edge_colors=colors))
```

Script can be rendered by any [gviz tool](https://dreampuf.github.io/GraphvizOnline/) online and the result can be following:

![gviz-example](https://raw.githubusercontent.com/JetBrains-Research/cuBool/master/docs/pictures/gviz_example.png)

## Contributors

- Egor Orachyov (Github: [EgorOrachyov](https://github.com/EgorOrachyov))
- Pavel Alimov (Github : [Krekep](https://github.com/Krekep))
- Semyon Grigorev (Github: [gsvgit](https://github.com/gsvgit))

## Citation 

```ignorelang
@MISC{cuBool,
  author = {Orachyov, Egor and Alimov, Pavel and Grigorev, Semyon},
  title = {cuBool: sparse Boolean linear algebra for Nvidia Cuda},
  year = 2021,
  url = {https://github.com/JetBrains-Research/cuBool},
  note = {Version 1.1.0}
}
```

## License

This project is licensed under MIT License. License text can be found in the 
[license file](https://github.com/JetBrains-Research/cuBool/blob/master/python/LICENSE.md).

## Acknowledgments

This is a research project of the Programming Languages and Tools Laboratory
at JetBrains-Research. Laboratory website [link](https://research.jetbrains.org/groups/plt_lab/).

## Also

The name of the library is formed by a combination of words *Cuda* and *Boolean*,
what literally means *Cuda with Boolean* and sounds very similar to the name of 
the programming language *COBOL*.