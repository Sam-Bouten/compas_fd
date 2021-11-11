import compas
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import NurbsCurve
from compas.geometry import NurbsSurface
from compas_fd.datastructures import CableMesh
from compas_fd.constraints import Constraint

from compas.rpc import Proxy

fofin = Proxy('compas_fd.fd')

constraints = [
    Constraint(Line([0, 0, 0], [1, 0, 0])),
    Constraint(Plane.worldXY()),
    Constraint(NurbsCurve.from_points([[0, 0, 0], [3, 6, 0], [6, -6, 6], [9, 0, 0]]))
]

mesh = CableMesh.from_meshgrid(dx=10, nx=10)

corners = list(mesh.vertices_where({'vertex_degree': 2}))

mesh.vertices_attribute('is_anchor', True, keys=corners)

for vertex in corners:
    mesh.vertex_attribute(vertex, 'constraint', constraints[0])

# for constraint in constraints:
#     s = compas.json_dumps(constraint)
#     print(s)
#     print(constraint)
#     print(constraint.data)
#     print(compas.json_loads(s))
#     # print(LineConstraint.from_data(constraint.data))

mesh = fofin.mesh_fd_numpy(mesh)

print(mesh)