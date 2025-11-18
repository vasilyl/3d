from build123d import *
from ocp_vscode import show, set_port


class Front(Part):
    def __init__(self):
        a, b = 40, 20

        l1 = JernArc(start=(0, 0), tangent=(0, 1), radius=a, arc_size=180)
        l2 = JernArc(start=l1 @ 1, tangent=l1 % 1, radius=a, arc_size=-90)
        l3 = Line(l2 @ 1, l2 @ 1 + (-a, a))
        ex14_ln = l1 + l2 + l3

        sk14 = Plane.XZ * Rectangle(b, b)
        ex14 = sweep(sk14, path=ex14_ln)
        super().__init__(shapes=[ex14])


if __name__ == "__main__":
    set_port(3939)
    root = Front()
    show(*root, names=[root.__class__.__name__])
