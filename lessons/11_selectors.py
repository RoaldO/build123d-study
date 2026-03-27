import marimo

__generated_with = "0.21.1"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    import marimo_cad as cad
    from build123d import Box, Cylinder, Align, Axis, GeomType, SortBy
    return Align, Axis, Box, Cylinder, GeomType, SortBy, cad, mo


@app.cell(column=0)
def _(mo):
    mo.md("""
    # Lesson 11 — Selectors

    After creating geometry you often need to select specific **edges**,
    **faces**, or **vertices** to apply operations like fillet, chamfer,
    or adding features on a face.

    ## Accessing topology

    ```python
    shape.edges()      # ShapeList of all edges
    shape.faces()      # ShapeList of all faces
    shape.vertices()   # ShapeList of all vertices
    ```

    ## filter_by

    Filter by geometry type or axis direction:

    ```python
    shape.edges().filter_by(Axis.Z)       # edges parallel to Z
    shape.faces().filter_by(Axis.Z)       # faces normal to Z (top/bottom)
    shape.edges().filter_by(GeomType.LINE)   # straight edges only
    shape.edges().filter_by(GeomType.CIRCLE) # circular edges only
    ```

    ## sort_by

    Sort the resulting list to pick a specific element:

    ```python
    shape.faces().sort_by(Axis.Z)[-1]   # topmost face
    shape.faces().sort_by(Axis.Z)[0]    # bottommost face
    ```

    ## Counting

    ```python
    len(shape.edges())    # how many edges?
    ```

    Selectors are used heavily in the next lesson (fillets/chamfers).
    """)
    return


@app.cell(column=0)
def _(mo):
    selector = mo.ui.dropdown(
        ["all edges", "Z edges", "circular edges", "top face"],
        value="all edges",
        label="Show selection",
    )
    selector
    return (selector,)


@app.cell(column=1)
def _(Align, Axis, Box, Cylinder, GeomType, cad, selector):
    from build123d import Mode, BuildPart

    with BuildPart() as part:
        box = Box(60, 40, 20, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with BuildPart():
            pass  # placeholder

    solid = Box(60, 40, 20, align=(Align.CENTER, Align.CENTER, Align.MIN))

    if selector.value == "all edges":
        sel = solid.edges()
    elif selector.value == "Z edges":
        sel = solid.edges().filter_by(Axis.Z)
    elif selector.value == "circular edges":
        cyl = Cylinder(20, 30)
        sel = cyl.edges().filter_by(GeomType.CIRCLE)
        solid = cyl
    else:
        sel = solid.faces().sort_by(Axis.Z)[-1:]

    count = len(sel)
    viewer = cad.Viewer()
    viewer.render(solid)
    viewer
    return BuildPart, Mode, count, part, sel, solid, viewer


@app.cell(column=1)
def _(count, mo, selector):
    mo.md(f"**{selector.value}** → `{count}` element(s) selected")
    return


@app.cell(column=0)
def _(mo):
    mo.md("""
    ## Exercise

    1. Count the faces of a `Box` and a `Cylinder`. Are the numbers what you
       expected?
    2. Select only the bottom face of a Box using `sort_by(Axis.Z)[0]`.
    3. On a `Cylinder`, use `filter_by(GeomType.PLANE)` — what do you get?
    4. Select the four vertical edges of a Box using `filter_by(Axis.Z)` and
       print the length of each.
    """)
    return


if __name__ == "__main__":
    app.run()
