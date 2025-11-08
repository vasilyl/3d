import cadquery as cq
from ocp_vscode import show, set_port

result = cq.Workplane("XY").box(10000, 7000, 5000)

assembly = cq.Assembly()
assembly.add(
    result,
    name="Result",
    # color=cq.Color(0.2, 0.4, 0.6) # Optional: Adds a color
)

assembly.export(path="result.glb")
assembly.export(path="result.vrml")

set_port(3939)
show(result)
