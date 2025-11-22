import build123d as b
from collections.abc import Iterable

from OCP.BRepBuilderAPI import (
    BRepBuilderAPI_MakeFace,
)
from OCP.BRepOffsetAPI import BRepOffsetAPI_MakeFilling
from OCP.GeomAbs import GeomAbs_C0
from OCP.gp import gp_Pnt
from OCP.Standard import (
    Standard_ConstructionError,
    Standard_Failure,
    Standard_NoSuchObject,
)
from OCP.StdFail import StdFail_NotDone

from build123d.geometry import (
    Vector,
    VectorLike,
)

from build123d.topology.one_d import Edge, Wire
from build123d.topology.shape_core import (
    ShapeList,
)


class Face(b.Face):
    @classmethod
    def make_surface(
        cls,
        exterior: Wire | Iterable[Edge],
        surface_points: Iterable[VectorLike] | None = None,
        interior_wires: Iterable[Wire] | None = None,
        energy: int = 3,
    ) -> b.Face:
        """Create Non-Planar Face

        Create a potentially non-planar face bounded by exterior (wire or edges),
        optionally refined by surface_points with optional holes defined by
        interior_wires.

        Args:
            exterior (Union[Wire, list[Edge]]): Perimeter of face
            surface_points (list[VectorLike], optional): Points on the surface that
                refine the shape. Defaults to None.
            interior_wires (list[Wire], optional): Hole(s) in the face. Defaults to None.

        Raises:
            RuntimeError: Internal error building face
            RuntimeError: Error building non-planar face with provided surface_points
            RuntimeError: Error adding interior hole
            RuntimeError: Generated face is invalid

        Returns:
            Face: Potentially non-planar face
        """
        exterior = list(exterior) if isinstance(exterior, Iterable) else exterior
        # pylint: disable=too-many-branches
        if surface_points:
            surface_point_vectors = [Vector(p) for p in surface_points]
        else:
            surface_point_vectors = None

        # First, create the non-planar surface
        surface = BRepOffsetAPI_MakeFilling(
            # order of energy criterion to minimize for computing the deformation of the surface
            Degree=energy,
        )
        if isinstance(exterior, Wire):
            outside_edges = exterior.edges()
        elif isinstance(exterior, Iterable) and all(
            isinstance(o, Edge) for o in exterior
        ):
            outside_edges = ShapeList(exterior)
        else:
            raise ValueError("exterior must be a Wire or list of Edges")

        for edge in outside_edges:
            if edge.wrapped is None:
                raise ValueError("exterior contains empty edges")
            surface.Add(edge.wrapped, GeomAbs_C0)

        try:
            surface.Build()
            surface_face = Face(surface.Shape())  # type:ignore[call-overload]
        except (
            Standard_Failure,
            StdFail_NotDone,
            Standard_NoSuchObject,
            Standard_ConstructionError,
        ) as err:
            raise RuntimeError(
                "Error building non-planar face with provided exterior"
            ) from err
        if surface_point_vectors:
            for point in surface_point_vectors:
                surface.Add(gp_Pnt(*point))
            try:
                surface.Build()
                surface_face = Face(surface.Shape())  # type:ignore[call-overload]
            except StdFail_NotDone as err:
                raise RuntimeError(
                    "Error building non-planar face with provided surface_points"
                ) from err

        # Next, add wires that define interior holes - note these wires must be entirely interior
        if interior_wires:
            makeface_object = BRepBuilderAPI_MakeFace(surface_face.wrapped)
            for wire in interior_wires:
                if wire.wrapped is None:
                    raise ValueError("interior_wires contain an empty wire")
                makeface_object.Add(wire.wrapped)
            try:
                surface_face = Face(makeface_object.Face())
            except StdFail_NotDone as err:
                raise RuntimeError(
                    "Error adding interior hole in non-planar face with provided interior_wires"
                ) from err

        surface_face = surface_face.fix()
        if not surface_face.is_valid:
            raise RuntimeError("non planar face is invalid")

        return surface_face
