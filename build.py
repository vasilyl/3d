import cadquery as cq
from cadquery import exporters
from ocp_vscode import show, set_port
import os

result = cq.Workplane("XY").box(2, 2, 4).faces(">Z").hole(1)
# Detect GitHub CI (or general CI) and disable interactive viewer in that environment
if os.getenv("GITHUB_ACTIONS", "").lower() == "true" or os.getenv("CI", "").lower() == "true":
    # Define the output directory and base filename
    OUTPUT_DIR = "exports"
    BASE_NAME = "result"

    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    views = {
        "top": "XY",
        "front": "XZ",
        "left": "YZ",
    }

    for name, plane_name in views.items():
        proj_workplane = cq.Workplane(plane_name) 
        
        projection = proj_workplane.add(result).section()
        
        exporters.export(
            projection, 
            os.path.join(OUTPUT_DIR, f"{BASE_NAME}_{name}.svg")
        )
    assembly = cq.Assembly()
    assembly.add(
        result,
        name="Result",
        # color=cq.Color(0.2, 0.4, 0.6) # Optional: Adds a color
    )

    assembly.export(path=f"{OUTPUT_DIR}/result.glb")
else:
    set_port(3939)
    show(result)
