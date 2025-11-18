from build123d import *
from ocp_vscode import show, set_port


class Front(Part):
    def __init__(self):
        super().__init__(
            [
                Box(1 * MM, 1 * MM, 1 * MM),
            ]
        )


if __name__ == "__main__":
    set_port(3939)
    root = Front()
    show(*root, names=[root.__class__.__name__])
