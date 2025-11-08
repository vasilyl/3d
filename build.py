import cadquery as cq
result = cq.Workplane("XY").box(10000, 7000, 5000)

assembly = cq.Assembly()
assembly.add(
    result,
    name="Result",
    # color=cq.Color(0.2, 0.4, 0.6) # Optional: Adds a color
)

assembly.export(path="result.glb")

result
