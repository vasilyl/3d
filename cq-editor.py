import cadquery as cq
result = cq.Workplane("XY").box(10000, 7000, 5000)

show_object(result)