from build123d import *
from ocp_vscode import show, set_port

from all import All

set_port(3939)

def project_to_2d(
    part: Part,
    viewport_origin: VectorLike,
    viewport_up: VectorLike,
    page_origin: VectorLike,
    scale_factor: float = 1.0,
) -> tuple[ShapeList[Edge], ShapeList[Edge]]:
    """project_to_2d

    Helper function to generate 2d views translated on the 2d page.

    Args:
        part (Part): 3d object
        viewport_origin (VectorLike): location of viewport
        viewport_up (VectorLike): direction of the viewport Y axis
        page_origin (VectorLike): center of 2d object on page
        scale_factor (float, optional): part scalar. Defaults to 1.0.

    Returns:
        tuple[ShapeList[Edge], ShapeList[Edge]]: visible & hidden edges
    """
    scaled_part = part if scale_factor == 1.0 else scale(part, scale_factor)
    visible, hidden = scaled_part.project_to_viewport(
        viewport_origin, viewport_up, look_at=(0, 0, 0)
    )
    visible = [Pos(*page_origin) * e for e in visible]
    hidden = [Pos(*page_origin) * e for e in hidden]

    return ShapeList(visible), ShapeList(hidden)


# The object that appearing in the drawing
part: Part = All().part()

# Create a standard technical drawing border on A3 paper
page_size = Vector(420 * MM, 297 * MM)
margin = 5 * MM
left_margin = 20 * MM
frame_size=page_size - Vector(left_margin + margin, 2 * margin)
frame = trace(lines=Wire.make_rect(frame_size.X, frame_size.Y))
page_rect = Wire.make_rect(page_size.X, page_size.Y).move(Pos(X=left_margin / -2))
page = trace(lines=page_rect, line_width=0.1)
border = Compound.make_compound([frame, page])

# Specify the drafting options for extension lines
drafting_options = Draft(
    line_width=0.1, font_size=3.5, decimal_precision=0, display_units=False
)

# Lists used to store the 2d visible and hidden lines
visible_lines, hidden_lines = [], []

# Isometric Projection - A 3D view where the part is rotated to reveal three
# dimensions equally.
iso_v, iso_h = project_to_2d(
    part,
    (100, 100, 100),
    (0, 0, 1),
    (1 / 4 * page_size.X, -1/4 * page_size.Y),
    # 0.75,
)
visible_lines.extend(iso_v)
hidden_lines.extend(iso_h)

# Front
vis, _ = project_to_2d(
    part,
    (0, -100, 0),
    (0, 0, 1),
    (-1 / 4 * page_size.X, 1 / 4 * page_size.Y),
)
visible_lines.extend(vis)
d3 = ExtensionLine(
    border=vis.sort_by(Axis.Y)[-1], offset=-5 * MM, draft=drafting_options
)

# Side
vis, _ = project_to_2d(
    part,
    (100, 0, 0),
    (0, 0, 1),
    (1 / 4 * page_size.X, 1 / 4 * page_size.Y),
)
visible_lines.extend(vis)
side_bbox = Curve(vis).bounding_box()
perimeter = Pos(*side_bbox.center()) * Rectangle(side_bbox.size.X, side_bbox.size.Y)
d4 = ExtensionLine(
    border=perimeter.edges().sort_by(Axis.X)[-1], offset=1 * CM, draft=drafting_options
)

# Plan View (Top)
vis, _ = project_to_2d(
    part,
    (0, 0, 100),
    (0, 1, 0),
    (-1 / 4 * page_size.X, -1/4 * page_size.Y),
)
visible_lines.extend(vis)

# Dimension
top_bbox = Curve(vis).bounding_box()
perimeter = Pos(*top_bbox.center()) * Rectangle(top_bbox.size.X, top_bbox.size.Y)
d1 = ExtensionLine(
    border=perimeter.edges().sort_by(Axis.X)[-1], offset=1 * CM, draft=drafting_options
)
d2 = ExtensionLine(
    border=perimeter.edges().sort_by(Axis.Y)[0], offset=1 * CM, draft=drafting_options
)

# Initialize the SVG exporter
exporter = ExportSVG(unit=Unit.MM)
# Define visible and hidden line layers
exporter.add_layer("Visible", fill_color=Export2D.DEFAULT_COLOR_INDEX, line_weight=1)
exporter.add_layer(
    "Hidden", line_color=Export2D.DEFAULT_COLOR_INDEX, line_type=LineType.HIDDEN
)
exporter.add_layer("Dimensions", fill_color=Export2D.DEFAULT_COLOR_INDEX, line_weight=0)
# Add the objects to the appropriate layer
exporter.add_shape(visible_lines, layer="Visible")
exporter.add_shape(hidden_lines, layer="Hidden")
exporter.add_shape(border, layer="Dimensions")
exporter.add_shape([d1, d2, d3, d4], layer="Dimensions")
# Write the file
exporter.write(f"exports/drawing.svg")

show(visible_lines, hidden_lines, d1, d2, d3, d4, border)
