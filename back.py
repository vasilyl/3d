from build123d import *
from ocp_vscode import *
from functools import reduce

from face import Face
import house


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

        stairs = extrude(plane * sketch, 1750 * MM)

        plane = Plane(origin=(0, lawn_from), x_dir=(1), z_dir=(0, -1, 0))
        sketch = Pos(1200 * MM) * Rectangle(1075 * MM, 140 * MM, align=Align.MIN) + Pos(
            1200 + 1075 * MM
        ) * Rectangle(3600 * MM, (140 + 130) * MM, align=Align.MIN)
        stairs += extrude(plane * sketch, lawn_from)

        side_line = Polyline(
            [
                (0, 18400 * MM, 230 * MM),
                (0, 19000 * MM, 270 * MM),
                (ret_wall_line @ 1) + Vector(0, 0, -550 * MM),
                (ret_wall_line @ 1) + Vector(0, -600 * MM, -850 * MM),
            ],
            close=True,
        )

        side = (
            extrude(
                Face.make_surface(side_line, energy=2), amount=550 * MM, dir=(0, 0, -1)
            )
            - ret_wall
        )

        gravel = (
            Pos(small_block.vertices().sort_by(SortBy.DISTANCE)[0])
            * Box(2810 * MM, 5660 * MM, 230 * MM, align=Align.MIN)
            - small_block
        )

        patio = Pos(
            gravel.vertices().group_by(Axis.Y)[-1].sort_by(SortBy.DISTANCE)[0]
        ) * Box(gravel.bounding_box().size.X, 3660 * MM, 350 * MM, align=Align.MIN)

        concrete = high_block + small_block + patio + stairs - ret_wall

        lower_lawn = (
            extrude(
                Face(
                    Polyline(
                        (0, lawn_from),
                        (5900 * MM, lawn_from),
                        (6650 * MM, 18620 * MM),
                        (0, 18400 * MM),
                        close=True,
                    )
                ),
                230 * MM,
            )
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
        offsets_from_start = [
            (450 * MM, 11300 * MM, -20 * MM),
            (340 * MM, 8500 * MM, -20 * MM),
            (250 * MM, 6500 * MM, -20 * MM),
            (160 * MM, 4500 * MM, -20 * MM),
            (80 * MM, 2500 * MM, -30 * MM),
            (10 * MM, 500 * MM, -100 * MM),
            (0, 0, -130 * MM),
        ]

        upper_lawn_line = (
            Polyline(
                [lawn_mulch_line @ 1]
                + [
                    ret_wall_short_edge.start_point() + off
                    for off in offsets_from_start
                ]
                + [
                    ret_wall_short_edge.end_point()
                    + (0, 0, -ret_wall_cap_height - ret_wall_block_height),
                ]
                + [
                    Pos(0, 0, 20 * MM),
                    Pos(0, 0, 0),
                ]
                * stairs_tops[-1]
                + [lawn_mulch_line @ 0]
            )
            + lawn_mulch_line
        )

        upper_lawn_base = Vector(stairs_tops[0].X, 0, 0)
        lawn_points = [
            (4 * M, 6 * M, 1260 * MM),
            (2 * M, -3 * M, 950 * MM),
            (2 * M, -4 * M, 1080 * MM),
        ]
        lawn_points = [v + upper_lawn_base for v in lawn_points]

        upper_lawn = (
            extrude(
                Face.make_surface(
                    upper_lawn_line, surface_points=lawn_points, energy=2
                ),
                2 * M,
                dir=(0, 0, -1),
            )
            - ret_wall
        )

        mulch_line = lawn_mulch_line + Polyline(
            lawn_mulch_line @ 1,
            (6900 * MM, 19230 * MM, 1080 * MM),
            (12200 * MM, 19400 * MM, 1700 * MM),
            (13000 * MM, -6730 * MM, 2200 * MM),
            (9850 * MM, -6800 * MM, 1950 * MM),
            (3845 * MM, -6870 * MM, 1500 * MM),
            (-4300 * MM, -7000 * MM, 950 * MM),
            (-4300 * MM, -6000 * MM, 930 * MM),
            (-4300 * MM, -4000 * MM, 835 * MM),
            (-4300 * MM, -2000 * MM, 740 * MM),
            (-4300 * MM, 0, 700 * MM),
            (3845 * MM, 0, 700 * MM),
            (3845 * MM, -2000 * MM, 740 * MM),
            lawn_mulch_line @ 0,
        )

        mulch_points = [
            (1690 * MM, -4000 * MM, 835 * MM),
            (1690 * MM, -6000 * MM, 990 * MM),
            (-300 * MM, -6000 * MM, 930 * MM),
            (-2300 * MM, -6000 * MM, 930 * MM),
        ]
        mulch = (
            extrude(
                Face.make_surface(mulch_line, energy=2, surface_points=mulch_points),
                2 * M,
                dir=(0, 0, -1),
            )
            - ret_wall
        )

        tsuga = Pos(12000 * MM, -6150 * MM, 2 * M) * Cylinder(
            radius=300 * MM,
            height=20 * M,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        tsuga.label = "Tsuga"
        camelia = Pos(3700 * MM, -6300 * MM) * Cylinder(
            radius=200 * MM, height=8 * M, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        camelia.label = "Camelia"
        plum = Pos(
            8650 * MM, house.BASEMENT.vertices().sort_by(Axis.Y)[-1].Y + 800 * MM, 1000 * MM
        ) * Cylinder(
            radius=60 * MM, height=6 * M, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        plum.label = "Plum"

        tree = Pos(
            12400 * MM,
            1500 * MM,
            1800 * MM,
        ) * Cylinder(
            radius=100 * MM, height=2 * M, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        tree.label = "Tree"

        thuja = Cone(
            bottom_radius=750 * MM,
            top_radius=0 * MM,
            height=5 * M,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        thujas = reduce(
            lambda a, b: a + b,
            (
                Pos(12 * M, y, 1700 * MM) * thuja
                for y in (7000 * MM, 8200 * MM, 9400 * MM, 10600 * MM)
            ),
        )
        thujas.label = "Thujas"

        concrete.color = "LightGray"
        lower_lawn.color = upper_lawn.color = patio.color = "Green"
        mulch.color = side.color = "SaddleBrown"
        gravel.color = ret_wall.color = "Gray"
        tsuga.color = camelia.color = plum.color = tree.color = thujas.color = (
            "DarkGreen"
        )

        super().__init__(
            children=[
                concrete,
                gravel,
                lower_lawn,
                ret_wall,
                upper_lawn,
                mulch,
                side,
                tsuga,
                camelia,
                plum,
                tree,
                thujas,
            ],
            label="Backyard",
        )


if __name__ == "__main__":
    set_port(3939)
    root = Back()
    show(*root, names=[f':{c.label}' for c in root.children], reset_camera=Camera.KEEP)
