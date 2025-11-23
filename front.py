from build123d import *
from ocp_vscode import *

from face import Face


class Front(Part):
    def __init__(self):
        lawn_line = Polyline(
            [
                (-4300 * MM, -665 * MM, 700 * MM),
                (-4300 * MM, -7000 * MM, 1000 * MM),
                (-17500 * MM, -7000 * MM, -200 * MM),
                (-17500 * MM, 6325 * MM, -550 * MM),
                (-11335 * MM, 6325 * MM, -50 * MM),
                (-11335 * MM, 3585 * MM, 360 * MM),
                (-7675 * MM, 3585 * MM, 700 * MM),
                (-7675 * MM, 1585 * MM, 700 * MM),
                (-7055 * MM, 945 * MM, 700 * MM),
                (-7055 * MM, -55 * MM, 700 * MM),
                (-6135 * MM, -55 * MM, 700 * MM),
                (-6135 * MM, -665 * MM, 700 * MM),
            ],
            close=True,
        )

        lawn = extrude(
            Face.make_surface(lawn_line, energy=2),
            amount=1000 * MM,
            dir=(0, 0, -1),
        ) + Pos(-11935 * MM, -715 * MM) * Cylinder(radius=1150 * MM, height=750 * MM)

        driveway_line = Polyline(
            [
                (-10115 * MM, 14045 * MM, -40 * MM),
                (-11335 * MM, 14045 * MM, -190 * MM),
                (-20515 * MM, 14045 * MM, -1830 * MM),
                #         (-20515 * MM, 11000 * MM, -1650 * MM),
                #         (-11335 * MM, 11000 * MM, -150 * MM),
                #         (-10115 * MM, 11000 * MM, -40 * MM),
                #     ],
                #     close=True,
                # ) + Polyline(
                #     [
                #         (-10115 * MM, 11000 * MM, -40 * MM),
                #         (-11335 * MM, 11000 * MM, -150 * MM),
                #         (-20515 * MM, 11000 * MM, -1650 * MM),
                (-20515 * MM, 7955 * MM, -1500 * MM),
                (-11335 * MM, 7955 * MM, -80 * MM),
                (-10115 * MM, 7955 * MM, -40 * MM),
            ],
            close=True,
        )

        driveway = extrude(
            Face.make_surface(driveway_line, energy=2),
            amount=200 * MM,
            dir=(0, 0, -1),
        )

        super().__init__(
            [
                lawn,
                driveway,
            ]
            # + [Pos(p) for p in surface_points] * Vertex()
        )


if __name__ == "__main__":
    set_port(3939)
    root = Front()
    show(*root, names=[root.__class__.__name__], reset_camera=Camera.KEEP)
