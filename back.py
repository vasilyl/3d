from build123d import *
from ocp_vscode import *


class Back(Part):

    def __init__(self):
        thickness = 210 * MM
        lawn_from = thickness + 1185 * MM
        length = 4055 * MM

        line = Line(
            (5750 * MM, -2460 * MM, 1080 * MM), (6650 * MM, 19220 * MM, 1080 * MM)
        )

        wall_profile = Plane(line @ 0, x_dir=1, z_dir=line @ 0 - line @ 1) * Sketch(
            [Rectangle(300 * MM, 75 * MM, align=Align.MAX)]
            + Locations([Pos(i * -20 * MM, -75 * MM - i * 155 * MM) for i in range(7)])
            * Rectangle(300 * MM, 155 * MM, align=Align.MAX)
        )
        ret_wall = sweep(wall_profile, line)

        high_wall = extrude(
            Rectangle(length, thickness, align=Align.MIN)
            + Pos(length, 0)
            * Rectangle(thickness, 2100 * MM, align=(Align.MAX, Align.MAX, Align.MIN)),
            780 * MM,
        )
        small_wall = Pos(0, lawn_from) * Box(
            2275 * MM, thickness, 530 * MM, align=Align.MIN
        )

        plane = Plane(origin=(length, -2100 * MM), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
        sketch = (
            Rectangle(400 * MM, 780 * MM, align=Align.MIN)
            + Pos(400 * MM) * Rectangle(955 * MM, (780 - 170) * MM, align=Align.MIN)
            + Pos((400 + 955) * MM)
            * Rectangle(955 * MM, (780 - 2 * 170) * MM, align=Align.MIN)
        )

        stairs = extrude(plane * sketch, 1500 * MM)

        plane = Plane(origin=(0, lawn_from), x_dir=(1), z_dir=(0, -1, 0))
        sketch = Pos(1200 * MM) * Rectangle(1075 * MM, 140 * MM, align=Align.MIN) + Pos(
            1200 + 1075 * MM
        ) * Rectangle(3400 * MM, (140 + 130) * MM, align=Align.MIN)
        stairs += extrude(plane * sketch, lawn_from)

        concrete = high_wall + small_wall + stairs - ret_wall

        gravel = (
            Pos(small_wall.vertices().sort_by(SortBy.DISTANCE).first)
            * Box(2810 * MM, 5660 * MM, 230 * MM, align=Align.MIN)
            - small_wall
        )

        patio = Pos(
            gravel.vertices().group_by(Axis.Y)[-1].sort_by(SortBy.DISTANCE).first
        ) * Box(gravel.bounding_box().size.X, 3660 * MM, 350 * MM, align=Align.MIN)

        lawn = (
            extrude(
                Face(Polyline(
                    (0, lawn_from),
                    (5700 * MM, lawn_from),
                    (6400 * MM, 19000 * MM),
                    (0, 19000 * MM),
                    close=True,
                )),
                230 * MM,
            )
            # Pos(0, lawn_from) * Box(6000 * MM, 17800 * MM, 230 * MM, align=Align.MIN)
            - ret_wall
            - small_wall
            - gravel
            - patio
        )

        super().__init__(
            [
                concrete,
                gravel,
                patio,
                lawn,
                ret_wall,
            ]
        )


if __name__ == "__main__":
    set_port(3939)
    root = Back()
    show(*root, names=[root.__class__.__name__], reset_camera=Camera.KEEP)
