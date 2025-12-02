from build123d import *
from ocp_vscode import show, set_port
import os

from all import All

_IS_BATCH = os.getenv("GITHUB_ACTIONS", "") == "true" or os.getenv("CI", "") == "true"
_OUTPUT_DIR = "public"

_DRAFT = Draft(line_width=0.1, font_size=3.5, decimal_precision=0, display_units=False)

_SCALE = 250


def project_to_2d(
    part: Part,
    viewport_origin: VectorLike,
    viewport_up: VectorLike,
    page_origin: VectorLike,
) -> tuple[ShapeList[Edge], ShapeList[Edge]]:
    """project_to_2d

    Helper function to generate 2d views translated on the 2d page.

    Args:
        part (Part): 3d object
        viewport_origin (VectorLike): location of viewport
        viewport_up (VectorLike): direction of the viewport Y axis
        page_origin (VectorLike): center of 2d object on page

    Returns:
        tuple[ShapeList[Edge], ShapeList[Edge]]: visible & hidden edges
    """
    scaled_part = part if _SCALE == 1.0 else scale(part, 1 / _SCALE)
    visible, hidden = scaled_part.project_to_viewport(
        viewport_origin, viewport_up, look_at=(0, 0, 0)
    )
    visible = [Pos(*page_origin) * e for e in visible]
    hidden = [Pos(*page_origin) * e for e in hidden]

    return ShapeList(visible), ShapeList(hidden)


def make_2d_drawing(part: Part) -> tuple[ShapeList[Edge], ShapeList[Edge], Compound]:
    # Create a standard technical drawing border on A3 paper
    page_size = Vector(420 * MM, 297 * MM)
    page = trace(lines=Rectangle(page_size.X, page_size.Y), line_width=0.1)
    margin = 5 * MM
    left_margin = 20 * MM
    frame_size = page_size - Vector(left_margin + margin, 2 * margin)
    frame = trace(
        lines=Pos((left_margin - margin) / 2) * Rectangle(frame_size.X, frame_size.Y)
    )
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
        (-50, 0, 0),
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
    bbox = Curve(vis).bounding_box()
    perimeter = Pos(*bbox.center()) * Rectangle(bbox.size.X, bbox.size.Y)
    by_x = perimeter.edges().sort_by(Axis.X)[-1]
    x_size = ExtensionLine(
        border=by_x, label=f"{by_x.length * _SCALE:.0f}", offset=1 * CM, draft=_DRAFT
    )
    by_y = perimeter.edges().sort_by(Axis.Y)[0]
    y_size = ExtensionLine(
        border=by_y, label=f"{by_y.length * _SCALE:.0f}", offset=1 * CM, draft=_DRAFT
    )

    # Isometric
    iso_v, iso_h = project_to_2d(
        part,
        (100, 100, 100),
        (0, 0, 1),
        (1 / 8 * page_size.X, -1 / 8 * page_size.Y),
    )
    visible.extend(iso_v)
    # hidden.extend(iso_h)
    border = Compound([frame, page, x_size, y_size])
    return visible, hidden, border


def export_3d(name: str, part: Part):
    export_gltf(part, f"{_OUTPUT_DIR}/{name}.gltf")
    export_gltf(part, f"{_OUTPUT_DIR}/{name}.glb", binary=True)
    export_stl(part, f"{_OUTPUT_DIR}/{name}.stl")


def export_2d(
    name: str, visible: ShapeList[Edge], hidden: ShapeList[Edge], border: Compound
) -> None:
    exporter = ExportSVG()
    # Define visible and hidden line layers
    exporter.add_layer(
        "Visible", fill_color=Export2D.DEFAULT_COLOR_INDEX, line_weight=0.5
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
    # Write the file
    os.makedirs(_OUTPUT_DIR, exist_ok=True)
    exporter.write(f"{_OUTPUT_DIR}/{name}.a3.svg")

    exporter = ExportDXF()
    # Define visible and hidden line layers
    exporter.add_layer("Visible", line_weight=0.5)
    exporter.add_layer("Hidden", line_type=LineType.HIDDEN)
    exporter.add_layer("Dimensions", line_weight=0)
    # Add the objects to the appropriate layer
    exporter.add_shape(visible, layer="Visible")
    exporter.add_shape(hidden, layer="Hidden")
    exporter.add_shape(border, layer="Dimensions")
    # Write the file
    os.makedirs(_OUTPUT_DIR, exist_ok=True)
    exporter.write(f"{_OUTPUT_DIR}/{name}.dxf")


_FORMATS = [
    "3D",
    "A3",
    # "Top",
    # "Iso",
    # "Front",
    # "Left",
]


def create_html_viewer(
    format: str, filename: str, label: str, parents: list[str], links: list[str]
) -> None:
    suffix = format.lower()
    inner = {
        "3D": f"""
             <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js"></script>
             <model-viewer alt="{format} - {label}" src="{filename}.glb" camera-controls shadow-intensity="1"
        environment-image="https://modelviewer.dev/shared-assets/environments/spruit_sunrise_1k_HDR.jpg"></model-viewer>""",
        "A3": f"""<img src="{filename}.{suffix}.svg" alt="{format} - {label}"/>""",
    }
    formats = [f'<a href="{filename}.{f.lower()}.html">{f}</a>' for f in _FORMATS]
    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>{format} Viewer - {label}</title>
        <link rel="stylesheet" href="main.css">
        </head>
        <body>
            <div id="menu">{''.join([f'<a href="{f}.{suffix}.html">{l}</a> / ' for l, f in parents])}<b>{label}</b>
            | {' '.join(links)}
            ({', '.join(formats)}, <a href="{filename}.stl">STL</a>, <a href="{filename}.dxf">DXF</a>)</div>
        {inner[format]}
        </body>
        </html>
        """
    with open(f"{_OUTPUT_DIR}/{filename}.{suffix}.html", "w") as suffix:
        suffix.write(html_content)


def generate(part: Part, parents: list[str] = []) -> None:
    label = part.label
    filename = part.__class__.__name__.lower().replace(" ", "_")
    if label:
        visible, hidden, border = make_2d_drawing(part)
        export_2d(filename, visible, hidden, border)
        export_3d(filename, part)
        result = [
            generate(e, parents + [(label, filename)])
            for e in part.children
            if e.label is not None
        ]
        for format in _FORMATS:
            links = [f'<a href="{f}.{format.lower()}.html">{l}</a>' for f, l in result]
            create_html_viewer(format, filename, label, parents, links)
    return filename, label


root = All()
generate(root)

if not _IS_BATCH:
    set_port(3939)
    show(*root)
