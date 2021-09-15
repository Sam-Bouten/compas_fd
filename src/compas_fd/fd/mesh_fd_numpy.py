from numpy import array
from numpy import float64

from .fd_numpy import fd_numpy

from compas_fd.loads import SelfweightCalculator


def mesh_fd_numpy(mesh):
    """Find the equilibrium shape of a mesh for the given force densities.

    Parameters
    ----------
    mesh : compas_fd.datastructures.CableMesh
        The mesh to equilibriate.

    Returns
    -------
    None
        The function updates the input mesh and returns nothing.

    """
    k_i = mesh.key_index()
    fixed = mesh.vertices_where({'is_anchor': True})
    fixed = [k_i[key] for key in fixed]
    xyz = array(mesh.vertices_attributes('xyz'), dtype=float64)
    p = array(mesh.vertices_attributes(('px', 'py', 'pz')), dtype=float64)
    edges = [(k_i[u], k_i[v]) for u, v in mesh.edges_where({'is_edge': True})]
    q = array([attr['q'] for key, attr in mesh.edges_where({'is_edge': True}, True)], dtype=float64).reshape((-1, 1))
    density = mesh.attributes['density']
    calculate_sw = SelfweightCalculator(mesh, density=density)
    p[:, 2] -= calculate_sw(xyz)

    result = fd_numpy(vertices=xyz, edges=edges, loads=p, q=q, fixed=fixed)

    for key, attr in mesh.vertices(True):
        index = k_i[key]
        attr['x'] = result.vertices[index, 0]
        attr['y'] = result.vertices[index, 1]
        attr['z'] = result.vertices[index, 2]
        attr['_rx'] = result.residuals[index, 0]
        attr['_ry'] = result.residuals[index, 1]
        attr['_rz'] = result.residuals[index, 2]

    for index, (key, attr) in enumerate(mesh.edges_where({'is_edge': True}, True)):
        attr['_f'] = result.forces[index, 0]
        attr['_l'] = result.lenghts[index, 0]