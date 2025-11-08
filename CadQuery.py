import cadquery as cq
from ocp_vscode import show, set_port

result = cq.Workplane("front").box(2.0, 2.0, 0.5)

set_port(3939)
show(result)