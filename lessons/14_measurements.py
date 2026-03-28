import marimo
import json
from pathlib import Path

try:
    _use_columns = json.loads((Path.home() / ".marimocad_prefs.json").read_text()).get("layout") == "columns"
except Exception:
    _use_columns = False

app = marimo.App(width="full" if _use_columns else "medium")


@app.cell
def _():
    import json
    import os as _os
    import marimo as mo
    import marimo_cad as cad
    from pathlib import Path as _P
    from build123d import (
        Box, Cylinder, fillet,
        Align, Axis, GeomType, Location, Vector,
    )
    import OCP.BRepAdaptor as _BRA

    try:
        use_columns = json.loads((_P.home() / ".marimocad_prefs.json").read_text()).get("layout") == "columns"
    except Exception:
        use_columns = False

    return Align, Axis, Box, Cylinder, GeomType, Location, Vector, _BRA, _P, _os, cad, fillet, mo, use_columns


@app.cell(hide_code=True)
def _(mo, _P, _os):
    _d = _P(str(mo.notebook_location()))
    _r = _P(_os.getcwd())
    _prev = f"/?file={(_d / '13_parametric_design.py').relative_to(_r)}"
    mo.md(f"""
    <small>[← 13]({_prev})</small>

    # Lesson 14 — Measurements and Inspection

    build123d provides a rich set of properties to inspect geometry: distances,
    areas, volumes, face normals, arc centers, and more. This lesson covers the
    most useful ones for practical CAD work.

    ## Basic properties

    | Property | Returns |
    |---|---|
    | `edge.length` | Length of an edge |
    | `face.area` | Surface area of a face |
    | `solid.volume` | Volume of a solid |
    | `shape.center()` | Centre of mass as `Vector` |
    | `vertex.center()` | Position of a vertex as `Vector` |

    ## Bounding box

    ```python
    bb = shape.bounding_box()
    bb.xmin, bb.xmax   # X extents
    bb.size            # Vector(xsize, ysize, zsize)
    bb.diagonal        # length of the space diagonal
    ```

    ## Distance between shapes

    ```python
    shape_a.distance_to(shape_b)   # minimum distance (float)
    ```

    Returns `0.0` when the shapes touch or overlap.

    ## Face normals and angles

    ```python
    face.normal_at()                       # outward normal at face centre
    face_a.normal_at().get_angle(face_b.normal_at())  # angle in degrees
    ```

    ## Arc properties

    For circular edges (`filter_by(GeomType.CIRCLE)`):

    ```python
    edge.arc_center   # Vector — centre of the circle
    edge.radius       # float — radius of the circle
    ```

    ## Fillet cylinder axis

    A fillet creates cylindrical faces. The axis of the fillet cylinder
    can be read via the OCP adaptor:

    ```python
    import OCP.BRepAdaptor as BRA

    cyl_face = shape.faces().filter_by(GeomType.CYLINDER)[0]
    adaptor  = BRA.BRepAdaptor_Surface(cyl_face.wrapped)
    ax       = adaptor.Cylinder().Axis()

    origin    = Vector(ax.Location().X(), ax.Location().Y(), ax.Location().Z())
    direction = Vector(ax.Direction().X(), ax.Direction().Y(), ax.Direction().Z())
    ```
    """)
    return


@app.cell
def _(mo):
    demo = mo.ui.dropdown(
        ["Basic properties", "Distance", "Face normals", "Arc + fillet axis"],
        value="Basic properties",
        label="Demo",
    )
    return (demo,)


@app.cell
def _(Align, Axis, Box, Cylinder, GeomType, Location, Vector, _BRA, cad, demo, fillet, mo, use_columns):
    solid = Box(60, 40, 20, align=(Align.CENTER, Align.CENTER, Align.MIN))
    filleted = fillet(solid.edges().filter_by(Axis.Z), 5)

    if demo.value == "Basic properties":
        bb = solid.bounding_box()
        lines = [
            f"**volume** = `{solid.volume:.1f} mm³`",
            f"**center** = `{solid.center()}`",
            f"**bbox**   = `{bb.xmin:.0f}…{bb.xmax:.0f}` × `{bb.ymin:.0f}…{bb.ymax:.0f}` × `{bb.zmin:.0f}…{bb.zmax:.0f}`",
            f"**diagonal** = `{bb.diagonal:.2f} mm`",
            f"**top face area** = `{solid.faces().sort_by(Axis.Z)[-1].area:.1f} mm²`",
            f"**longest edge** = `{max(e.length for e in solid.edges()):.1f} mm`",
        ]
        shape = solid

    elif demo.value == "Distance":
        cyl = Cylinder(8, 30).move(Location((50, 0, 15)))
        dist = solid.distance_to(cyl)
        lines = [
            f"**distance** box → cylinder = `{dist:.2f} mm`",
            "",
            "_Move the cylinder closer by changing its X position in the code._",
        ]
        shape = solid + cyl

    elif demo.value == "Face normals":
        faces = solid.faces()
        angles = []
        top = faces.sort_by(Axis.Z)[-1]
        for f in faces:
            a = top.normal_at().get_angle(f.normal_at())
            angles.append(f"  normal `{f.normal_at()}` — angle to top face: **{a:.0f}°**")
        lines = angles
        shape = solid

    else:  # Arc + fillet axis
        arcs = filleted.edges().filter_by(GeomType.CIRCLE)
        cyl_faces = filleted.faces().filter_by(GeomType.CYLINDER)
        adaptor = _BRA.BRepAdaptor_Surface(cyl_faces[0].wrapped)
        ax = adaptor.Cylinder().Axis()
        origin    = Vector(ax.Location().X(), ax.Location().Y(), ax.Location().Z())
        direction = Vector(ax.Direction().X(), ax.Direction().Y(), ax.Direction().Z())
        lines = [
            f"**circular edges** = `{len(arcs)}`",
            f"**arc radius** = `{arcs[0].radius:.1f} mm`",
            f"**arc center** (first) = `{arcs[0].arc_center}`",
            "",
            f"**fillet cylinder axis origin** = `{origin}`",
            f"**fillet cylinder axis direction** = `{direction}`",
        ]
        shape = filleted

    info = mo.md("\n\n".join(lines))
    viewer = cad.Viewer()
    viewer.render(shape)
    controls = mo.vstack([demo, info])
    mo.hstack([controls, viewer], widths=[1, 3]) if use_columns else mo.vstack([controls, viewer])
    return adaptor, arcs, ax, bb, cyl_faces, direction, dist, f, faces, filleted, info, lines, origin, shape, solid, top, viewer


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise

    1. Build a `Cylinder` and measure its volume — verify the result against
       the formula $V = \\pi r^2 h$.
    2. Place two boxes apart and measure the distance between them. Move them
       closer until `distance_to` returns `0`.
    3. Create a box with a fillet on the vertical edges. Read the `arc_center`
       of all circular edges and verify they form the four corners of the
       original box outline.
    4. Extract the fillet cylinder axis for all four fillets and confirm the
       direction is `(0, 0, 1)` in each case.
    5. **Challenge**: compute the angle between two adjacent side faces of a
       box that has had one edge chamfered at 45°.
    """)
    return


if __name__ == "__main__":
    app.run()
