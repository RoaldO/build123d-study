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
        BuildPart, BuildSketch, extrude,
        Box, Cylinder, Circle, Rectangle,
        Plane, Location, Locations, Axis, Align,
    )

    try:
        use_columns = json.loads((_P.home() / ".marimocad_prefs.json").read_text()).get("layout") == "columns"
    except Exception:
        use_columns = False

    return Align, Axis, Box, BuildPart, BuildSketch, Circle, Cylinder, Location, Locations, Plane, Rectangle, _P, _os, cad, extrude, mo, use_columns


@app.cell(hide_code=True)
def _(mo, _P, _os):
    _d = _P(str(mo.notebook_location()))
    _r = _P(_os.getcwd())
    _prev = f"/?file={(_d / '09_sketches.py').relative_to(_r)}"
    _next = f"/?file={(_d / '11_locations.py').relative_to(_r)}"
    mo.md(f"""
    <small>[← 09]({_prev}) &nbsp;·&nbsp; [11 →]({_next})</small>

    # Lesson 10 — Positioning in the Builder API

    A very common source of confusion when using `BuildPart` and `BuildSketch`
    is that features unexpectedly land at the origin. This happens because
    **every sketch is placed on a workplane**, and the default workplane is
    `Plane.XY` — the XY plane at Z = 0.

    Understanding workplanes is the key to controlling where geometry goes.

    ## The default workplane

    ```python
    with BuildPart() as part:
        with BuildSketch():          # ← Plane.XY at Z=0 (default)
            Circle(10)
        extrude(amount=5)            # extrudes upward from Z=0
    ```

    ## Offset planes

    Use `Plane.XY.offset(z)` to start the sketch at a different height:

    ```python
    with BuildPart() as part:
        with BuildSketch(Plane.XY.offset(20)):   # start at Z=20
            Circle(10)
        extrude(amount=5)
    ```

    ## Sketching on an existing face

    Pass a face as the workplane. The sketch sits on that face and extrude
    goes outward:

    ```python
    with BuildPart() as part:
        Box(40, 40, 20)
        with BuildSketch(part.faces().sort_by(Axis.Z)[-1]):  # top face
            Circle(10)
        extrude(amount=10)
    ```

    ## XY position within a sketch

    Use `Locations` *inside* `BuildSketch` to shift the sketch origin in 2D:

    ```python
    with BuildPart() as part:
        Box(60, 60, 10)
        with BuildSketch(part.faces().sort_by(Axis.Z)[-1]):
            with Locations([(15, 0), (-15, 0)]):
                Circle(8)
        extrude(amount=8)
    ```

    ## Named planes

    | Plane | Normal direction |
    |---|---|
    | `Plane.XY` | Z (default) |
    | `Plane.XZ` | Y |
    | `Plane.YZ` | X |
    | `Plane.XY.offset(z)` | Z, shifted up |
    | `Plane(origin, x_dir, normal)` | custom |
    """)
    return


@app.cell
def _(mo):
    method = mo.ui.dropdown(
        options={
            "Default (Plane.XY)":       "default",
            "Offset plane":             "offset",
            "Sketch on top face":       "face",
            "2D offset with Locations": "locations_2d",
        },
        value="Default (Plane.XY)",
        label="Positioning method",
    )
    return (method,)


@app.cell
def _(Axis, Box, BuildPart, BuildSketch, Circle, Locations, Plane, cad, extrude, method, mo, use_columns):
    from build123d import Mode

    with BuildPart() as part:
        Box(60, 60, 20)

        if method.value == "default":
            # Common mistake: sketch lands at Z=0, extrude goes up through the base
            with BuildSketch():
                Circle(12)
            extrude(amount=10, mode=Mode.ADD)

        elif method.value == "offset":
            # Place sketch at the top of the box (Z=20)
            with BuildSketch(Plane.XY.offset(20)):
                Circle(12)
            extrude(amount=10)

        elif method.value == "face":
            # Use the actual top face as workplane
            with BuildSketch(part.faces().sort_by(Axis.Z)[-1]):
                Circle(12)
            extrude(amount=10)

        else:
            # Two bosses offset in X on the top face
            with BuildSketch(part.faces().sort_by(Axis.Z)[-1]):
                with Locations([(15, 0), (-15, 0)]):
                    Circle(8)
            extrude(amount=10)

    viewer = cad.Viewer()
    viewer.render(part.part)

    _notes = {
        "default":      "⚠ Sketch is at Z=0 — the cylinder passes **through** the base.",
        "offset":       "✓ `Plane.XY.offset(20)` places the sketch exactly at the top surface.",
        "face":         "✓ Using the top face as workplane — always follows the geometry.",
        "locations_2d": "✓ Two bosses placed with `Locations` inside the sketch.",
    }
    info = mo.callout(mo.md(_notes[method.value]), kind="warn" if method.value == "default" else "info")
    controls = mo.vstack([method, info])
    mo.hstack([controls, viewer], widths=[1, 3]) if use_columns else mo.vstack([controls, viewer])
    return Mode, info, part, viewer


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise

    1. Start with a `Box(60, 40, 15)`. Add a cylindrical boss on the top face
       using `BuildSketch(part.faces().sort_by(Axis.Z)[-1])`. Confirm it sits
       on top and not inside the box.
    2. Replace the face selector with `Plane.XY.offset(15)`. Do you get the
       same result? When would they differ?
    3. Add four bosses arranged in a rectangle using `Locations` inside the
       sketch. Hint: `Locations([(x1,y1), (x2,y1), (x1,y2), (x2,y2)])`.
    4. Sketch on `Plane.XZ` instead of `Plane.XY`. What changes?
    5. **Challenge**: build a box, add a cylinder on the top, then add a second
       smaller cylinder on *top of the first cylinder* by selecting its top face.
    """)
    return


if __name__ == "__main__":
    app.run()
