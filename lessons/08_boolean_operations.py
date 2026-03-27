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
    from build123d import Box, Cylinder, Sphere, Location, Align

    try:
        use_columns = json.loads((Path.home() / ".marimocad_prefs.json").read_text()).get("layout") == "columns"
    except Exception:
        use_columns = False

    return Align, Box, Cylinder, Location, Sphere, cad, mo, use_columns


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
    return (op,)


@app.cell
def _(Align, Box, Cylinder, Location, cad, mo, op, use_columns):
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

    controls = mo.vstack([op])
    mo.hstack([controls, viewer], widths=[1, 3]) if use_columns else mo.vstack([controls, viewer])
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



@app.cell(hide_code=True)
def _(mo):
    import shutil
    from pathlib import Path as _Path

    _name = "08_boolean_operations.py"
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
