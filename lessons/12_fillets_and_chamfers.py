import marimo

__generated_with = "0.21.1"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    import marimo_cad as cad
    from build123d import Box, Cylinder, fillet, chamfer, Align, Axis, GeomType
    return Align, Axis, Box, Cylinder, GeomType, cad, chamfer, fillet, mo


@app.cell(column=0)
def _(mo):
    mo.md("""
    # Lesson 12 — Fillets and Chamfers

    Fillets and chamfers are applied to **edges** selected from a solid.

    ## fillet

    Rounds an edge with a circular profile.

    ```python
    result = fillet(shape.edges(), radius)
    result = fillet(shape.edges().filter_by(Axis.Z), radius)
    ```

    ## chamfer

    Cuts an edge at 45° (equal length on both sides by default).

    ```python
    result = chamfer(shape.edges(), length)
    result = chamfer(shape.edges(), length, length2)  # asymmetric
    ```

    ## Selecting the right edges

    | Goal | Selector |
    |---|---|
    | All edges | `shape.edges()` |
    | Vertical edges | `shape.edges().filter_by(Axis.Z)` |
    | Top edge ring | `shape.faces().sort_by(Axis.Z)[-1].edges()` |
    | Circular edges | `shape.edges().filter_by(GeomType.CIRCLE)` |

    ## Tip

    Start with a large radius and reduce it — fillet errors are often caused
    by a radius that is too large for the geometry.
    """)
    return


@app.cell(column=0)
def _(mo):
    op      = mo.ui.radio(["fillet", "chamfer"], value="fillet", label="Operation")
    target  = mo.ui.radio(["all", "vertical", "top ring"], value="vertical", label="Edge selection")
    size    = mo.ui.slider(1, 10, value=3, label="Radius / Length")
    mo.vstack([op, target, size])
    return op, size, target


@app.cell(column=1)
def _(Axis, Box, Align, GeomType, cad, chamfer, fillet, op, size, target):
    solid = Box(60, 40, 25, align=(Align.CENTER, Align.CENTER, Align.MIN))

    if target.value == "all":
        edges = solid.edges()
    elif target.value == "vertical":
        edges = solid.edges().filter_by(Axis.Z)
    else:
        edges = solid.faces().sort_by(Axis.Z)[-1].edges()

    try:
        if op.value == "fillet":
            result = fillet(edges, size.value)
        else:
            result = chamfer(edges, size.value)
        viewer = cad.Viewer()
        viewer.render(result)
    except Exception as e:
        viewer = cad.Viewer()
        viewer.render(solid)

    viewer
    return edges, result, solid, viewer


@app.cell(column=0)
def _(mo):
    mo.md("""
    ## Exercise

    1. Fillet only the four vertical edges of a box (use `filter_by(Axis.Z)`).
    2. Chamfer the top ring of edges using
       `faces().sort_by(Axis.Z)[-1].edges()`.
    3. Combine: fillet the vertical edges, then chamfer the top ring.
       Remember — apply operations in sequence on the result.
    4. On a `Cylinder`, fillet the circular top edge. What radius limit do
       you encounter?
    """)
    return


if __name__ == "__main__":
    app.run()
