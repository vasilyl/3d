from build123d import *
from ocp_vscode import *

from back import Back
from front import Front
from house import House


class All(Part):
    def __init__(self):
        super().__init__(
            children=[
                House(),
                Front(),
                Back(),
            ],
            label="All",
        )


if __name__ == "__main__":
    set_port(3939)
    root = All()
    show(*root, names=[f':{c.label}' for c in root.children], reset_camera=Camera.KEEP)
