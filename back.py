from build123d import *
from ocp_vscode import *

from face import Face


class Back(Part):

    def __init__(self):
        thickness = 210 * MM
        lawn_from = thickness + 1185 * MM
        length = 4055 * MM

        ret_wall_block_width = 300 * MM
        ret_wall_block_height = 155 * MM
        ret_wall_cap_height = 75 * MM

        ret_wall_line = Line(
            (5755 * MM, -2460 * MM, 1080 * MM), (6650 * MM, 19220 * MM, 1080 * MM)
        )

        wall_profile = Plane(
            ret_wall_line @ 0, x_dir=1, z_dir=ret_wall_line @ 0 - ret_wall_line @ 1
        ) * Sketch(
            [
                Rectangle(
                    ret_wall_block_width,
                    ret_wall_cap_height,
                    align=(Align.MIN, Align.MAX),
                )
            ]
            + Locations(
                [
                    Pos(i * -20 * MM, -ret_wall_cap_height - i * ret_wall_block_height)
                    for i in range(7)
                ]
            )
            * Rectangle(
                ret_wall_block_width,
                ret_wall_block_height,
                align=(Align.MIN, Align.MAX),
            )
        )
        ret_wall = sweep(wall_profile, ret_wall_line)

        high_block = extrude(
            Rectangle(length, thickness, align=Align.MIN)
            + Pos(length, 0)
            * Rectangle(thickness, 2100 * MM, align=(Align.MAX, Align.MAX, Align.MIN)),
            780 * MM,
        )
        small_block = Pos(0, lawn_from) * Box(
            2275 * MM, thickness, 530 * MM, align=Align.MIN
        )

        plane = Plane(origin=(length, -2100 * MM), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
        sketch = (
            Rectangle(400 * MM, 780 * MM, align=Align.MIN)
            + Pos(400 * MM) * Rectangle(955 * MM, (780 - 170) * MM, align=Align.MIN)
            + Pos((400 + 955) * MM)
            * Rectangle(955 * MM, (780 - 2 * 170) * MM, align=Align.MIN)
        )

        stairs = extrude(plane * sketch, 1700 * MM)

        plane = Plane(origin=(0, lawn_from), x_dir=(1), z_dir=(0, -1, 0))
        sketch = Pos(1200 * MM) * Rectangle(1075 * MM, 140 * MM, align=Align.MIN) + Pos(
            1200 + 1075 * MM
        ) * Rectangle(3400 * MM, (140 + 130) * MM, align=Align.MIN)
        stairs += extrude(plane * sketch, lawn_from)

        concrete = high_block + small_block + stairs - ret_wall

        gravel = (
            Pos(small_block.vertices().sort_by(SortBy.DISTANCE)[0])
            * Box(2810 * MM, 5660 * MM, 230 * MM, align=Align.MIN)
            - small_block
        )

        patio = Pos(
            gravel.vertices().group_by(Axis.Y)[-1].sort_by(SortBy.DISTANCE)[0]
        ) * Box(gravel.bounding_box().size.X, 3660 * MM, 350 * MM, align=Align.MIN)

        lower_lawn = (
            extrude(
                Face(
                    Polyline(
                        (0, lawn_from),
                        (5700 * MM, lawn_from),
                        (6400 * MM, 19000 * MM),
                        (0, 19000 * MM),
                        close=True,
                    )
                ),
                230 * MM,
            )
            # Pos(0, lawn_from) * Box(6000 * MM, 17800 * MM, 230 * MM, align=Align.MIN)
            - ret_wall
            - small_block
            - gravel
            - patio
        )
        stairs_tops = (
            concrete.vertices().group_by(Axis.Y)[0].group_by(Axis.Z)[-1].sort_by(Axis.X)
        )
        ret_wall_short_edge = ret_wall.edges().group_by(Axis.Z)[-1].sort_by(Axis.Y)[0]

        lawn_mulch_line = (
            Polyline(
                [
                    Pos(0, 0, -30 * MM),
                    Pos(0, -900 * MM, 20 * MM),
                    Pos(0, -1900 * MM, 170 * MM),
                    Pos(0, -2900 * MM, 250 * MM),
                    Pos(0, -3400 * MM, 300 * MM),
                    Pos(2 * M, -3400 * MM, 410 * MM),
                ]
                * stairs_tops[0],
            )
            + Polyline(
                [
                    Pos(2 * M, -3400 * MM, 410 * MM),
                    Pos(3 * M, -3400 * MM, 450 * MM),
                    Pos(4 * M, -3100 * MM, 450 * MM),
                    Pos(6 * M, -2400 * MM, 450 * MM),
                    Pos(6500 * MM, -1700 * MM, 450 * MM),
                    Pos(6500 * MM, -900 * MM, 450 * MM),
                    Pos(6500 * MM, 100 * MM, 450 * MM),
                ]
                * stairs_tops[0],
                # tangents=[(1, 0, 0), (0, 1, 0)],
            )
            + Polyline(
                [
                    Pos(6500 * MM, 100 * MM, 450 * MM) * stairs_tops[0],
                    (10350 * MM, 8900 * MM, 1380 * MM),
                    (11200 * MM, 18500 * MM, 1230 * MM),
                    (6900 * MM, 18500 * MM, 1020 * MM),
                ]
            )
        )
        upper_lawn_line = (
            Polyline(
                [
                    (6900 * MM, 18500 * MM, 1020 * MM),
                    ret_wall_short_edge.start_point()
                    + (450 * MM, 11300 * MM, -20 * MM),
                    ret_wall_short_edge.start_point() + (340 * MM, 8500 * MM, -20 * MM),
                    ret_wall_short_edge.start_point() + (250 * MM, 6500 * MM, -20 * MM),
                    ret_wall_short_edge.start_point() + (160 * MM, 4500 * MM, -20 * MM),
                    ret_wall_short_edge.start_point() + (80 * MM, 2500 * MM, -30 * MM),
                    ret_wall_short_edge.start_point() + (10 * MM, 500 * MM, -100 * MM),
                    ret_wall_short_edge.start_point() + (0, 0, -130 * MM),
                    ret_wall_short_edge.end_point()
                    + (0, 0, -ret_wall_cap_height - ret_wall_block_height),
                ]
                + [
                    Pos(0, 0, 20 * MM),
                    Pos(0, 0, 0),
                ]
                * stairs_tops[-1]
                + [
                    Pos(0, 0, -30 * MM),
                ]
                * stairs_tops[0]
            )
            + lawn_mulch_line
        )

        upper_lawn_base = Vector(stairs_tops[0].X, 0, 0)
        surface_points = [
            (4 * M, 6 * M, 1260 * MM),
            (2 * M, -3 * M, 950 * MM),
            (2 * M, -4 * M, 1080 * MM),
        ]
        surface_points = [v + upper_lawn_base for v in surface_points]

        upper_lawn = Face.make_surface(
            upper_lawn_line, surface_points=surface_points, energy=2
        )

        super().__init__(
            [
                concrete,
                gravel,
                patio,
                lower_lawn,
                ret_wall,
                -upper_lawn,
            ]
            # + [Pos(p) for p in surface_points] * Vertex()
        )


if __name__ == "__main__":
    set_port(3939)
    root = Back()
    show(*root, names=[root.__class__.__name__], reset_camera=Camera.KEEP)
