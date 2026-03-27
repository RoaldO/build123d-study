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
    from build123d import Box, Cylinder, Align, Axis, GeomType

    try:
        use_columns = json.loads((Path.home() / ".marimocad_prefs.json").read_text()).get("layout") == "columns"
    except Exception:
        use_columns = False

    return Align, Axis, Box, Cylinder, GeomType, cad, mo, use_columns


@app.cell
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
    shape.edges().filter_by(Axis.Z)            # edges parallel to Z
    shape.faces().filter_by(Axis.Z)            # faces normal to Z (top/bottom)
    shape.edges().filter_by(GeomType.LINE)     # straight edges only
    shape.edges().filter_by(GeomType.CIRCLE)   # circular edges only
    ```

    ## sort_by

    Sort the resulting list to pick a specific element:

    ```python
    shape.faces().sort_by(Axis.Z)[-1]   # topmost face
    shape.faces().sort_by(Axis.Z)[0]    # bottommost face
    ```
    """)
    return


@app.cell
def _(mo):
    selector = mo.ui.dropdown(
        ["all edges", "Z edges", "circular edges", "top face"],
        value="all edges",
        label="Show selection",
    )
    return (selector,)


@app.cell
def _(Align, Axis, Box, Cylinder, GeomType, cad, mo, selector, use_columns):
    solid = Box(60, 40, 20, align=(Align.CENTER, Align.CENTER, Align.MIN))

    if selector.value == "all edges":
        sel = solid.edges()
        shape = solid
    elif selector.value == "Z edges":
        sel = solid.edges().filter_by(Axis.Z)
        shape = solid
    elif selector.value == "circular edges":
        shape = Cylinder(20, 30)
        sel = shape.edges().filter_by(GeomType.CIRCLE)
    else:
        sel = solid.faces().sort_by(Axis.Z)[-1:]
        shape = solid

    count = len(sel)
    viewer = cad.Viewer()
    viewer.render(shape)

    info = mo.md(f"**{selector.value}** → `{count}` element(s) selected")
    controls = mo.vstack([selector, info])
    mo.hstack([controls, viewer], widths=[1, 3]) if use_columns else mo.vstack([controls, viewer])
    return count, sel, shape, solid, viewer


@app.cell
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



@app.cell(hide_code=True)
def _(mo):
    import shutil
    from pathlib import Path as _Path

    _name = "11_selectors.py"
    _src = _Path(str(mo.notebook_location())) / _name
    _dst = _Path(str(mo.notebook_location())).parent / "workspace" / _name

    def _do_copy(v):
        _dst.parent.mkdir(exist_ok=True)
        shutil.copy2(_src, _dst)
        return v + 1

    copy_btn = mo.ui.button(
        label="Copy lesson to workspace",
        on_click=_do_copy,
        value=0,
    )
    copy_btn
    return (copy_btn,)


@app.cell(hide_code=True)
def _(copy_btn, mo):
    if copy_btn.value > 0:
        _out = mo.callout(
            mo.md("Copied! Open the file from the `workspace/` folder to start the exercise."),
            kind="success",
        )
    else:
        _out = mo.md("")
    _out


if __name__ == "__main__":
    app.run()
