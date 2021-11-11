import compas
from compas.geometry import Vector, Plane, Point, Line
from compas_fd.datastructures import CableMesh

from compas_fd.constraints import Constraint
from compas_fd.numdata import FDNumericalData
from compas_fd.solvers import FDConstraintSolver

from compas_view2.app import App
from compas_view2.objects import Object, MeshObject

Object.register(CableMesh, MeshObject)

mesh = CableMesh.from_obj(compas.get('faces.obj'))

mesh.vertices_attribute('is_anchor', True, keys=list(mesh.vertices_where({'vertex_degree': 2})))
mesh.vertices_attribute('t', 0.0)

# line constraint
vertex = list(mesh.vertices_where({'x': 10, 'y': 10}))[0]
line = Line(Point(10, 0, 0), Point(5, 10, 5))
constraint = Constraint(line)
mesh.vertex_attribute(vertex, 'constraint', constraint)

# plane constraint
vertex = list(mesh.vertices_where({'x': 0, 'y': 0}))[0]
plane = Plane((-1, 0, 0), (2, 1, -1))
constraint = Constraint(plane)
mesh.vertex_attribute(vertex, 'constraint', constraint)

# input solver parameters
vertex_index = mesh.vertex_index()
vertices = mesh.vertices_attributes('xyz')
fixed = list(mesh.vertices_where({'is_anchor': True}))
edges = [(vertex_index[u], vertex_index[v]) for
         u, v in mesh.edges_where({'_is_edge': True})]
forcedensities = mesh.edges_attribute('q')
loads = mesh.vertices_attributes(['px', 'py', 'pz'])
constraints = list(mesh.vertices_attribute('constraint'))

# set up iterative constraint solver
numdata = FDNumericalData.from_params(vertices, fixed, edges, forcedensities, loads)
solver = FDConstraintSolver(numdata, constraints, kmax=30,
                            tol_res=1E-3, tol_disp=1E-3)

# run solver
result = solver()
print(solver.iter_count)

# update mesh
for index, vertex in enumerate(mesh.vertices()):
    mesh.vertex_attributes(vertex, 'xyz', result.vertices[index])
    mesh.vertex_attributes(vertex, ['_rx', '_ry', '_rz'], result.residuals[index])


# ==============================================================================
# Viz
# ==============================================================================

viewer = App()

viewer.add(mesh)

for vertex in fixed:
    viewer.add(Point(* mesh.vertex_attributes(vertex, 'xyz')), size=20, color=(0, 0, 0))

for constraint in constraints:
    if constraint:
        viewer.add(constraint.geometry, linewidth=5, linecolor=(0, 1, 1))

for vertex in fixed:
    a = Point(* mesh.vertex_attributes(vertex, 'xyz'))
    b = a - Vector(* mesh.vertex_attributes(vertex, ['_rx', '_ry', '_rz']))
    viewer.add(Line(a, b), linewidth=3, linecolor=(0, 0, 1))

viewer.run()
