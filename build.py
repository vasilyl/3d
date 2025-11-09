import cadquery as cq
from ocp_vscode import show, set_port
import os

result = cq.Workplane("XY").box(2, 2, 4).faces(">Z").hole(1)

# Detect GitHub CI (or general CI) and disable interactive viewer in that environment
if os.getenv("GITHUB_ACTIONS", "").lower() == "true" or os.getenv("CI", "").lower() == "true":
    assembly = cq.Assembly()
    assembly.add(
        result,
        name="Result",
        # color=cq.Color(0.2, 0.4, 0.6) # Optional: Adds a color
    )

    assembly.export(path="result.glb")
else:
    set_port(3939)
    show(result)
