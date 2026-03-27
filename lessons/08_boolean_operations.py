import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import marimo_cad as cad
    from build123d import Box, Cylinder, Sphere, Location, Align
    return Align, Box, Cylinder, Location, Sphere, cad, mo


@app.cell
def _(mo):
    mo.md("""
    # Lesson 08 — Boolean Operations

    The three fundamental boolean operations let you combine and subtract solids.

    | Operation | Operator | Function |
    |---|---|---|
    | Union | `a + b` | Merge two solids |
    | Subtraction | `a - b` | Remove b from a |
    | Intersection | `a & b` | Keep only the overlap |

    All three return a new `Solid` and leave the inputs unchanged.

    ## Tip: positioning before combining

    Use `Location((x, y, z))` to move a shape before applying a boolean:

    ```python
    hole = Cylinder(5, 30).move(Location((10, 0, 0)))
    result = box - hole
    ```

    `.move(loc)` returns a new shape at the given position.
    """)
    return


@app.cell
def _(mo):
    op = mo.ui.radio(["Union", "Subtract", "Intersect"], value="Union", label="Operation")
    op
    return (op,)


@app.cell
def _(Align, Box, Cylinder, Location, cad, op):
    base = Box(50, 50, 20, align=(Align.CENTER, Align.CENTER, Align.MIN))
    tool = Cylinder(18, 30).move(Location((0, 0, 0)))

    if op.value == "Union":
        result = base + tool
    elif op.value == "Subtract":
        result = base - tool
    else:
        result = base & tool

    viewer = cad.Viewer()
    viewer.render(result)
    viewer
    return base, result, tool, viewer


@app.cell
def _(mo):
    mo.md("""
    ## Exercise

    1. Subtract three cylinders from the box to create mounting holes at the
       four corners.
    2. Use union to stack a smaller box on top of the base, then subtract a
       cylinder through both.
    3. Create a sphere and intersect it with a box — what shape do you get?
    """)
    return


if __name__ == "__main__":
    app.run()
