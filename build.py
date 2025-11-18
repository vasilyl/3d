from build123d import *
from ocp_vscode import show, set_port
import os

from all import All

_IS_BATCH = os.getenv("GITHUB_ACTIONS", "") == "true" or os.getenv("CI", "") == "true"
_OUTPUT_DIR = "public"


def project_to_2d(
    part: Part,
    viewport_origin: VectorLike,
    viewport_up: VectorLike,
    page_origin: VectorLike,
    scale_factor: float = .005,
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


def make_2d_drawing(part: Part) -> tuple[ShapeList[Edge], ShapeList[Edge], Compound]:
    # Create a standard technical drawing border on A3 paper
    page_size = Vector(420 * MM, 297 * MM)
    margin = 5 * MM
    left_margin = 20 * MM
    frame_size = page_size - Vector(left_margin + margin, 2 * margin)
    frame = trace(lines=Wire.make_rect(frame_size.X, frame_size.Y))
    page_rect = Wire.make_rect(page_size.X, page_size.Y).move(Pos(X=left_margin / -2))
    page = trace(lines=page_rect, line_width=0.1)
    border = Compound([frame, page])
    visible, hidden = [], []
    # Front
    vis, _ = project_to_2d(
        part,
        (0, -50, 0),
        (0, 0, 1),
        (-1 / 4 * page_size.X, 1 / 4 * page_size.Y),
    )
    visible.extend(vis)

    # Side
    vis, _ = project_to_2d(
        part,
        (50, 0, 0),
        (0, 0, 1),
        (1 / 4 * page_size.X, 1 / 4 * page_size.Y),
    )
    visible.extend(vis)

    # Top
    vis, _ = project_to_2d(
        part,
        (0, 0, 50),
        (0, 1, 0),
        (-1 / 4 * page_size.X, -1 / 4 * page_size.Y),
    )
    visible.extend(vis)

    # Isometric
    iso_v, iso_h = project_to_2d(
        part,
        (100, 100, 100),
        (0, 0, 1),
        (1 / 4 * page_size.X, -1 / 4 * page_size.Y),
    )
    visible.extend(iso_v)
    hidden.extend(iso_h)
    return visible, hidden, border


def save_drawing_as_svg(
    name: str, visible: ShapeList[Edge], hidden: ShapeList[Edge], border: Compound
) -> None:
    # Initialize the SVG exporter
    exporter = ExportSVG(unit=Unit.MM)
    # Define visible and hidden line layers
    exporter.add_layer(
        "Visible", fill_color=Export2D.DEFAULT_COLOR_INDEX, line_weight=1
    )
    exporter.add_layer(
        "Hidden", line_color=Export2D.DEFAULT_COLOR_INDEX, line_type=LineType.HIDDEN
    )
    exporter.add_layer(
        "Dimensions", fill_color=Export2D.DEFAULT_COLOR_INDEX, line_weight=0
    )
    # Add the objects to the appropriate layer
    exporter.add_shape(visible, layer="Visible")
    exporter.add_shape(hidden, layer="Hidden")
    exporter.add_shape(border, layer="Dimensions")
    # exporter.add_shape([d1, d2, d3, d4], layer="Dimensions")
    # Write the file
    os.makedirs(_OUTPUT_DIR, exist_ok=True)
    exporter.write(f"{_OUTPUT_DIR}/{name}.svg")


def create_html_viewer(filename: str, label: str) -> None:
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <title>Drawing Viewer - {label}</title>
      <style>
      html, body {{
        height: 100%;
        margin: 0;
      }}
      img {{
        display: block;
        margin: 0 auto;
        max-width: 100%;
        height: auto;
      }}
      </style>
    </head>
    <body>
    <img src="{filename}.svg" alt="Drawing - {label}"/>
    </body>
    </html>
    """
    with open(f"{_OUTPUT_DIR}/{filename}.html", "w") as f:
        f.write(html_content)


def generate(part: Part) -> None:
    part.label = part.label if part.label else part.__class__.__name__
    filename = part.label.lower().replace(" ", "_")
    visible, hidden, border = make_2d_drawing(part)
    save_drawing_as_svg(filename, visible, hidden, border)
    create_html_viewer(
        filename,
        part.label,
    )
    [generate(e) for e in part.children]


root = All()
generate(root)

if not _IS_BATCH:
    set_port(3939)
    show(*root)
