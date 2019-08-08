from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numpy import array
from numpy import float64

from compas.numerical import dr_numpy


__all__ = ['unload_numpy']


def unload_numpy(mesh, kmax=10000, tol=0.01):
    """"""
    key_index = mesh.key_index()
    uv_index  = {(u, v): index for index, (u, v) in enumerate(mesh.edges_where({'is_edge': True}))}

    fixed  = [key_index[key] for key in mesh.vertices_where({'is_anchor': True})]
    xyz    = array(mesh.get_vertices_attributes('xyz'), dtype=float64)
    p      = array([[0.0, 0.0, 0.0] for _ in range(len(xyz))], dtype=float64)
    edges  = [(key_index[u], key_index[v]) for u, v in mesh.edges_where({'is_edge': True})]
    qpre   = array([0.0] * len(edges), dtype=float64).reshape((-1, 1))
    fpre   = array([0.0] * len(edges), dtype=float64).reshape((-1, 1))
    lpre   = array([0.0] * len(edges), dtype=float64).reshape((-1, 1))
    l0     = array([attr['l0'] for u, v, attr in mesh.edges_where({'is_edge': True}, True)], dtype=float64).reshape((-1, 1))
    E      = array([attr['E'] * 1e+6 for u, v, attr in mesh.edges_where({'is_edge': True}, True)], dtype=float64).reshape((-1, 1))
    radius = array([attr['r'] for u, v, attr in mesh.edges_where({'is_edge': True}, True)], dtype=float64).reshape((-1, 1))

    xyz, q, f, l, r = dr_numpy(xyz, edges, fixed, p, qpre, fpre, lpre, l0, E, radius, kmax=kmax, tol1=tol)

    for key, attr in mesh.vertices(True):
        index = key_index[key]
        attr['x'] = xyz[index, 0]
        attr['y'] = xyz[index, 1]
        attr['z'] = xyz[index, 2]
        attr['rx'] = r[index, 0]
        attr['ry'] = r[index, 1]
        attr['rz'] = r[index, 2]

    for u, v, attr in mesh.edges_where({'is_edge': True}, True):
        index = uv_index[(u, v)]
        attr['f'] = f[index, 0]
        attr['l'] = l[index, 0]


        # ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
