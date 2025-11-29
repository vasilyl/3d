from build123d import *
from ocp_vscode import *

BASEMENT = Box(7055 * MM, 14100 * MM, 6 * M, align=(Align.MAX, Align.MIN, Align.MIN))
CHIMNEY = Pos(-14 * FT) * Box(
    6 * FT, 2 * FT, 7 * M, align=(Align.MAX, Align.MAX, Align.MIN)
)


class House(Part):
    def __init__(self):
        basement_length = 14100 * MM
        basement_width = 7055 * MM
        garage_length = 6090 * MM
        garage_width = 3060 * MM
        house = (
            Box(
                basement_width,
                basement_length,
                6 * M,
                align=(Align.MAX, Align.MIN, Align.MIN),
            )
        )

        garage = Pos(-basement_width, basement_length) * Box(
            garage_width,
            garage_length,
            3 * M,
            align=(Align.MAX, Align.MAX, Align.MIN),
        )
        super().__init__([BASEMENT + CHIMNEY + garage])


if __name__ == "__main__":
    set_port(3939)
    root = House()
    show(*root, names=[root.__class__.__name__], reset_camera=Camera.KEEP)
