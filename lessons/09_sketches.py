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
    import marimo as mo
    import marimo_cad as cad
    from pathlib import Path
    from build123d import (
        BuildPart, BuildSketch, extrude, revolve,
        Circle, Rectangle, RegularPolygon, Ellipse,
        SlotCenterToCenter, Plane, Axis,
    )

    try:
        use_columns = json.loads((Path.home() / ".marimocad_prefs.json").read_text()).get("layout") == "columns"
    except Exception:
        use_columns = False

    return (
        Axis, BuildPart, BuildSketch, Circle, Ellipse,
        Plane, Rectangle, RegularPolygon, SlotCenterToCenter,
        cad, extrude, mo, revolve, use_columns,
    )


@app.cell(hide_code=True)
def _(mo):
    import os as _os
    from pathlib import Path as _P
    _d = _P(str(mo.notebook_location()))
    _r = _P(_os.getcwd())
    _prev = f"/?file={(_d / '08_boolean_operations.py').relative_to(_r)}"
    _next = f"/?file={(_d / '10_positioning.py').relative_to(_r)}"
    mo.md(f"""
    <small>[← 08]({_prev}) &nbsp;·&nbsp; [10 →]({_next})</small>

    # Lesson 09 — Sketches and Extrude

    build123d uses a **builder API** for sketch-based modelling.

    ## Workflow

    ```python
    with BuildPart() as part:
        with BuildSketch():
            Rectangle(40, 20)
            Circle(8, mode=Mode.SUBTRACT)  # hole
        extrude(amount=10)
    ```

    `BuildSketch` accumulates 2D geometry. Shapes added with
    `mode=Mode.SUBTRACT` cut away from the sketch.

    `extrude(amount=...)` turns the sketch into a 3D solid.

    ## Common 2D shapes

    | Shape | Signature |
    |---|---|
    | `Rectangle` | `Rectangle(width, height)` |
    | `Circle` | `Circle(radius)` |
    | `RegularPolygon` | `RegularPolygon(radius, side_count)` |
    | `Ellipse` | `Ellipse(x_radius, y_radius)` |
    | `SlotCenterToCenter` | `SlotCenterToCenter(center_span, height)` |

    ## Revolve

    Instead of `extrude`, use `revolve(axis=Axis.Y)` to spin the sketch
    around an axis — useful for turned parts.
    """)
    return


@app.cell
def _(mo):
    op     = mo.ui.radio(["Extrude", "Revolve"], value="Extrude", label="Operation")
    width  = mo.ui.slider(20, 100, value=60, label="Width")
    height = mo.ui.slider(5,  60,  value=30, label="Height / Depth")
    hole_r = mo.ui.slider(0,  20,  value=8,  label="Hole radius (0 = none)")
    return height, hole_r, op, width


@app.cell
def _(
    Axis, BuildPart, BuildSketch, Circle, Rectangle,
    cad, extrude, height, hole_r, mo, op, revolve, use_columns, width,
):
    from build123d import Mode

    with BuildPart() as part:
        with BuildSketch():
            Rectangle(width.value, height.value)
            if hole_r.value > 0:
                Circle(hole_r.value, mode=Mode.SUBTRACT)
        if op.value == "Extrude":
            extrude(amount=height.value)
        else:
            revolve(axis=Axis.Y)

    viewer = cad.Viewer()
    viewer.render(part.part)

    controls = mo.vstack([op, width, height, hole_r])
    mo.hstack([controls, viewer], widths=[1, 3]) if use_columns else mo.vstack([controls, viewer])
    return Mode, part, viewer


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise

    1. Replace the `Rectangle` with a `RegularPolygon` (hexagon). Extrude it.
    2. Sketch a `SlotCenterToCenter` and extrude it — this is a common shape
       for mounting slots.
    3. Use `revolve` on a rectangle that does not cross the Y axis to make a
       tube or disc.
    """)
    return



if __name__ == "__main__":
    app.run()
