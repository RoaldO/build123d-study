import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import marimo_cad as cad
    from build123d import Box, Cylinder, Sphere, Cone, Torus, Location
    return Box, Cone, Cylinder, Location, Sphere, Torus, cad, mo


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
    shape_choice
    return (shape_choice,)


@app.cell
def _(Box, Cone, Cylinder, Sphere, Torus, cad, shape_choice):
    shapes = {
        "Box":      Box(40, 30, 20),
        "Cylinder": Cylinder(20, 40),
        "Sphere":   Sphere(25),
        "Cone":     Cone(20, 5, 40),
        "Torus":    Torus(30, 8),
    }
    viewer = cad.Viewer()
    viewer.render(shapes[shape_choice.value])
    viewer
    return shapes, viewer


@app.cell
def _(mo):
    mo.md("""
    ## Exercise

    1. Add sliders to control the dimensions of each primitive. Connect them
       so the correct sliders appear for the selected shape (`mo.ui.dropdown`
       + `if` logic).
    2. Use `align=(Align.CENTER, Align.CENTER, Align.MIN)` on the Box so it
       sits on the XY plane — observe the difference in the viewer.
    3. Create a `Cylinder` with `radius=5` and `height=50`. Place a copy at
       `Location((30, 0, 0))`. Render both as a named dict.
    """)
    return


if __name__ == "__main__":
    app.run()
