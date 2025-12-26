from build123d import *
from ocp_vscode import *

from face import Face
import house


class Front(Part):
    def __init__(self):
        fence_pole = Box(4 * IN, 4 * IN, 2 * M)
        chimney_corner = (
            house.CHIMNEY.vertices()
            .group_by(Axis.X)[-1]
            .group_by(Axis.Y)[0]
            .sort_by(Axis.Z)[0]
        )
        lawn_corner = Pos(-fence_pole.width) * chimney_corner
        lawn_line = Polyline(
            [
                Pos(0, 0, 700 * MM) * lawn_corner,
                (lawn_corner.X, -7000 * MM, 1000 * MM),
                (-17500 * MM, -7000 * MM, -200 * MM),
                (-17500 * MM, 6380 * MM, -550 * MM),
                (-11335 * MM, 6380 * MM, -50 * MM),
                (-11335 * MM, 3640 * MM, 360 * MM),
                (-8500 * MM, 3640 * MM, 700 * MM),
                (-8500 * MM, -house.CHIMNEY.width, 700 * MM),
            ],
            close=True,
        )

        lawn = extrude(
            Face.make_surface(lawn_line, energy=2),
            amount=1000 * MM,
            dir=(0, 0, -1),
        )

        maple = Pos(-11935 * MM, -715 * MM, 700 * MM) * (
            Cylinder(radius=1150 * MM, height=750 * MM)
            + Cylinder(
                radius=100 * MM,
                height=2 * M,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
        )

        stairs_top = Pos(-10115 * MM, 6380 * MM, -250 * MM)
        driveway_line = Polyline(
            [
                (-10115 * MM, 46 * FT, -40 * MM),
                (-10115 * MM - 4 * FT, 46 * FT, -190 * MM),
                (-20515 * MM, 46 * FT, -1830 * MM),
                #         (-20515 * MM, 36 * FT, -1650 * MM),
                #         (-11335 * MM, 36 * FT, -150 * MM),
                #         (-10115 * MM, 36 * FT, -40 * MM),
                #     ],
                #     close=True,
                # ) + Polyline(
                #     [
                #         (-10115 * MM, 36 * FT, -40 * MM),
                #         (-11335 * MM, 36 * FT, -150 * MM),
                #         (-20515 * MM, 36 * FT, -1650 * MM),
                (-20515 * MM, 26 * FT, -1500 * MM),
                (-10115 * MM - 4 * FT, 26 * FT, -80 * MM),
                (-10115 * MM - 4 * FT, stairs_top.position.Y + 4 * FT, -55 * MM),
                (-10115 * MM - 8 * FT, stairs_top.position.Y + 4 * FT, -100 * MM),
                (-10115 * MM - 8 * FT, stairs_top.position.Y, -100 * MM),
                (-10115 * MM - 4 * FT, stairs_top.position.Y, 25 * MM),
                (-10115 * MM - 4 * FT, 3640 * MM + 8 * FT, 40 * MM),
                (-10115 * MM, 3640 * MM + 8 * FT, 50 * MM),
                (-10115 * MM, 26 * FT, -40 * MM),
            ],
            close=True,
        )

        driveway = extrude(
            Face.make_surface(driveway_line, energy=2),
            amount=200 * MM,
            dir=(0, 0, -1),
        )

        stair0 = extrude(
            Face.make_surface(
                Polyline(
                    [
                        (0, 0, -900 * MM),
                        (-1860 * MM, 0, -1170 * MM),
                        (-1860 * MM, 4 * FT, -1220 * MM),
                        (0, 4 * FT, -920 * MM),
                    ],
                    close=True,
                ),
                energy=2,
            ),
            amount=200 * MM,
            dir=(0, 0, -1),
        )

        stair = extrude(
            Face.make_surface(
                Polyline(
                    [
                        (0, 0, 0),
                        (-4 * FT, 0, -40 * MM),
                        (-4 * FT, 4 * FT, -40 * MM),
                        (0, 4 * FT, 0),
                    ],
                    close=True,
                ),
                energy=2,
            ),
            amount=200 * MM,
            dir=(0, 0, -1),
        )

        stair1 = Pos(stairs_top.position.X - 4 * FT, 3640 * MM + 4 * FT) * extrude(
            Face.make_surface(
                Polyline(
                    [
                        (0, 0, 215 * MM),
                        (4 * FT, 0, 235 * MM),
                        (4 * FT, 4 * FT, 195 * MM),
                        (0, 4 * FT, 195 * MM),
                    ],
                    close=True,
                ),
                energy=2,
            ),
            amount=200 * MM,
            dir=(0, 0, -1),
        )

        stair2 = Pos(stairs_top.position.X - 4 * FT, 3640 * MM) * extrude(
            Face.make_surface(
                Polyline(
                    [
                        (0, 0, 360 * MM),
                        (4 * FT, 0, 375 * MM),
                        (4 * FT, 4 * FT, 370 * MM),
                        (0, 4 * FT, 355 * MM),
                    ],
                    close=True,
                ),
                energy=2,
            ),
            amount=200 * MM,
            dir=(0, 0, -1),
        )

        stair3 = Pos(stairs_top.position.X, 3640 * MM) * extrude(
            Face.make_surface(
                Polyline(
                    [
                        (0, 0, 515 * MM),
                        (4 * FT, 0, 535 * MM),
                        (4 * FT, 4 * FT, 535 * MM),
                        (0, 4 * FT, 515 * MM),
                    ],
                    close=True,
                ),
                energy=2,
            ),
            amount=200 * MM,
            dir=(0, 0, -1),
        )

        stair4 = Pos(stairs_top.position.X + 4 * FT, 3640 * MM) * extrude(
            Face.make_surface(
                Polyline(
                    [
                        (0, 0, 685 * MM),
                        (4 * FT, 0, 700 * MM),
                        (6 * FT, 2 * FT, 700 * MM),
                        (6 * FT, 4 * FT, 700 * MM),
                        (0, 4 * FT, 685 * MM),
                    ],
                    close=True,
                ),
                energy=2,
            ),
            amount=200 * MM,
            dir=(0, 0, -1),
        )

        stairs = (
            stair1
            + stairs_top
            * (
                Pos(-8 * FT, 0, 0) * stair
                + Pos(-12 * FT, 0, -7.2 * IN) * stair
                + Pos(-16 * FT, 0, -2 * 7.2 * IN) * stair
                + Pos(-20 * FT, 0, -3 * 7.2 * IN) * stair
                + Pos(-24 * FT, 0, -4 * 7.2 * IN) * stair
                + Pos(-28 * FT) * stair0
            )
            + stair2
            + stair3
            + stair4
        )

        douglas_fir = (
            Pos(-3 * FT, -4500 * MM, 500 * MM)
            * Pos(chimney_corner)
            * Cylinder(
                radius=500 * MM,
                height=15 * M,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
        )

        buxus = Pos(
            -13330 * MM,
            4800 * MM,
        ) * Sphere(radius=400 * MM, align=(Align.CENTER, Align.CENTER, Align.MIN))
        buxus.color = "DarkGreen"
        buxus.label = "Buxus"

        concrete = driveway + stairs

        concrete.color = "LightGray"
        maple.color = douglas_fir.color = "Gray"
        maple.label = "Maple"
        douglas_fir.label = "Douglas Fir"
        lawn.color = "Green"

        super().__init__(
            children=[
                lawn,
                concrete,
                maple,
                douglas_fir,
                buxus,
            ],
            label="Front yard",
        )


if __name__ == "__main__":
    set_port(3939)
    root = Front()

    show(*root, names=[f':{c.label}' for c in root.children], reset_camera=Camera.KEEP)
