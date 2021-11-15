import compas_fd

from compas_fd.numdata import FDNumericalData
from compas_fd.solvers import FDConstraintSolver


def mesh_fd_constraint_numpy(mesh: 'compas_fd.datastructures.CableMesh') -> 'compas_fd.datastructures.CableMesh':
    """Iteratively find the equilibrium shape of a mesh for the given force densities.

    Parameters
    ----------
    mesh : :class:`compas_fd.datastructures.CableMesh`
        The mesh to equilibriate.

    Returns
    -------
    :class:`compas_fd.datastructures.CableMesh`
        The function updates the mesh in place,
        but returns a reference to the updated mesh as well
        for compatibility with RPCs.

    """
    numdata = FDNumericalData.from_mesh(mesh)
    constraints = list(c for c in mesh.vertices_attribute('constraint') if c)
    solver = FDConstraintSolver(numdata, constraints,
                                kmax=100, tol_res=1E-3, tol_disp=1E-3)
    result = solver()
    _update_mesh(mesh, result)
    return mesh


def _update_mesh(mesh, result):
    for key, attr in mesh.vertices(True):
        index = mesh.key_index()[key]
        attr['x'] = result.vertices[index, 0]
        attr['y'] = result.vertices[index, 1]
        attr['z'] = result.vertices[index, 2]
        attr['_rx'] = result.residuals[index, 0]
        attr['_ry'] = result.residuals[index, 1]
        attr['_rz'] = result.residuals[index, 2]

    for index, (key, attr) in enumerate(mesh.edges_where({'_is_edge': True}, True)):
        attr['_f'] = result.forces[index, 0]
        attr['_l'] = result.lenghts[index, 0]