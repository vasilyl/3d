from build123d import *
from build123d import PathDescriptor
from ocp_vscode import show, set_port


class House(Part):
    def __init__(self):
        basement_length = 14100 * MM
        basement_width = 7055 * MM
        garage_length = 6090 * MM
        garage_width = 3060 * MM
        house = Box(
            basement_width,
            basement_length,
            6 * M,
            align=(Align.MAX, Align.MIN, Align.MIN),
        )
        house.color = "red"

        garage = Pos(-basement_width, basement_length) * Box(
            garage_width,
            garage_length,
            3 * M,
            align=(Align.MAX, Align.MAX, Align.MIN),
        )
        super().__init__(shapes=[house + garage])


if __name__ == "__main__":
    set_port(3939)
    root = House()
    show(*root, names=[root.__class__.__name__])
