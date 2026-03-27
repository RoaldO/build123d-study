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
    from build123d import Box, Cylinder, Sphere, Cone, Torus

    try:
        use_columns = json.loads((Path.home() / ".marimocad_prefs.json").read_text()).get("layout") == "columns"
    except Exception:
        use_columns = False

    return Box, Cone, Cylinder, Sphere, Torus, cad, mo, use_columns


@app.cell
def _(mo):
    mo.md("""
    # Lesson 07 — Primitives

    build123d ships a set of solid primitives you can use directly or combine
    with boolean operations (next lesson).

    | Primitive | Signature |
    |---|---|
    | `Box` | `Box(length, width, height)` |
    | `Cylinder` | `Cylinder(radius, height)` |
    | `Sphere` | `Sphere(radius)` |
    | `Cone` | `Cone(bottom_radius, top_radius, height)` |
    | `Torus` | `Torus(major_radius, minor_radius)` |

    All primitives are **centred on the origin** by default. Use the `align`
    parameter or `Location` to reposition them.

    ## Alignment

    ```python
    from build123d import Align
    Box(10, 10, 5, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # bottom face sits on the XY plane
    ```
    """)
    return


@app.cell
def _(mo):
    shape_choice = mo.ui.dropdown(
        ["Box", "Cylinder", "Sphere", "Cone", "Torus"],
        value="Box",
        label="Primitive",
    )
    return (shape_choice,)


@app.cell
def _(Box, Cone, Cylinder, Sphere, Torus, cad, mo, shape_choice, use_columns):
    shapes = {
        "Box":      Box(40, 30, 20),
        "Cylinder": Cylinder(20, 40),
        "Sphere":   Sphere(25),
        "Cone":     Cone(20, 5, 40),
        "Torus":    Torus(30, 8),
    }
    viewer = cad.Viewer()
    viewer.render(shapes[shape_choice.value])

    controls = mo.vstack([shape_choice])
    mo.hstack([controls, viewer], widths=[1, 3]) if use_columns else mo.vstack([controls, viewer])
    return shapes, viewer


@app.cell
def _(mo):
    mo.md("""
    ## Exercise

    1. Add sliders to control the dimensions of each primitive. Connect them
       so the correct sliders appear for the selected shape (`if` logic).
    2. Use `align=(Align.CENTER, Align.CENTER, Align.MIN)` on the Box so it
       sits on the XY plane — observe the difference in the viewer.
    3. Create a `Cylinder` with `radius=5` and `height=50`. Place a copy at
       `Location((30, 0, 0))`. Render both as a named dict.
    """)
    return


if __name__ == "__main__":
    app.run()
