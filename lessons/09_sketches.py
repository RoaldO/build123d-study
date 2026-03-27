import marimo

__generated_with = "0.21.1"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    import marimo_cad as cad
    from build123d import (
        BuildPart, BuildSketch, extrude, revolve,
        Circle, Rectangle, RegularPolygon, Ellipse,
        SlotCenterToCenter, Plane, Axis,
    )
    return (
        Axis, BuildPart, BuildSketch, Circle, Ellipse,
        Plane, Rectangle, RegularPolygon, SlotCenterToCenter,
        cad, extrude, mo, revolve,
    )


@app.cell(column=0)
def _(mo):
    mo.md("""
    # Lesson 09 — Sketches and Extrude

    build123d uses a **builder API** for sketch-based modelling.

    ## Workflow

    ```python
    with BuildPart() as part:
        with BuildSketch() as sk:
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


@app.cell(column=0)
def _(mo):
    op = mo.ui.radio(["Extrude", "Revolve"], value="Extrude", label="Operation")
    width  = mo.ui.slider(20, 100, value=60, label="Width")
    height = mo.ui.slider(5,  60,  value=30, label="Height / Depth")
    hole_r = mo.ui.slider(0,  20,  value=8,  label="Hole radius (0 = none)")
    mo.vstack([op, width, height, hole_r])
    return height, hole_r, op, width


@app.cell(column=1)
def _(
    Axis, BuildPart, BuildSketch, Circle, Plane,
    Rectangle, cad, extrude, height, hole_r, op, revolve,
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
    viewer
    return Mode, part, viewer


@app.cell(column=0)
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
