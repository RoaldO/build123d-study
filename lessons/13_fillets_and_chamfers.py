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
    from build123d import Box, Cylinder, fillet, chamfer, Align, Axis, GeomType

    try:
        use_columns = json.loads((Path.home() / ".marimocad_prefs.json").read_text()).get("layout") == "columns"
    except Exception:
        use_columns = False

    return Align, Axis, Box, GeomType, cad, chamfer, fillet, mo, use_columns


@app.cell(hide_code=True)
def _(mo):
    import os as _os
    from pathlib import Path as _P
    _d = _P(str(mo.notebook_location()))
    _r = _P(_os.getcwd())
    _prev = f"/?file={(_d / '12_selectors.py').relative_to(_r)}"
    _next = f"/?file={(_d / '14_parametric_design.py').relative_to(_r)}"
    mo.md(f"""
    <small>[← 12]({_prev}) &nbsp;·&nbsp; [14 →]({_next})</small>

    # Lesson 13 — Fillets and Chamfers

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

    Start with a small radius and increase it — fillet errors are often caused
    by a radius that is too large for the geometry.
    """)
    return


@app.cell
def _(mo):
    op     = mo.ui.radio(["fillet", "chamfer"], value="fillet", label="Operation")
    target = mo.ui.radio(["all", "vertical", "top ring"], value="vertical", label="Edge selection")
    size   = mo.ui.slider(1, 10, value=3, label="Radius / Length")
    return op, size, target


@app.cell
def _(Align, Axis, Box, cad, chamfer, fillet, mo, op, size, target, use_columns):
    solid = Box(60, 40, 25, align=(Align.CENTER, Align.CENTER, Align.MIN))

    if target.value == "all":
        edges = solid.edges()
    elif target.value == "vertical":
        edges = solid.edges().filter_by(Axis.Z)
    else:
        edges = solid.faces().sort_by(Axis.Z)[-1].edges()

    try:
        result = fillet(edges, size.value) if op.value == "fillet" else chamfer(edges, size.value)
    except Exception:
        result = solid

    viewer = cad.Viewer()
    viewer.render(result)

    controls = mo.vstack([op, target, size])
    mo.hstack([controls, viewer], widths=[1, 3]) if use_columns else mo.vstack([controls, viewer])
    return edges, result, solid, viewer


@app.cell(hide_code=True)
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
