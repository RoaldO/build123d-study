import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import marimo_cad as cad
    from build123d import (
        Box, Cylinder, Location, Locations,
        GridLocations, PolarLocations, Align, Axis,
    )
    return Align, Axis, Box, Cylinder, GridLocations, Location, Locations, PolarLocations, cad, mo


@app.cell
def _(mo):
    mo.md("""
    # Lesson 10 — Locations and Positioning

    Positioning shapes is one of the most important skills in build123d.

    ## Location

    `Location((x, y, z))` — translate only.
    `Location((x, y, z), (rx, ry, rz))` — translate + rotate (degrees).

    ```python
    shape.move(Location((10, 0, 0)))        # move in X
    shape.move(Location((0, 0, 0), (0, 0, 45)))  # rotate 45° around Z
    ```

    ## Locations context manager

    Place the same geometry at multiple positions at once:

    ```python
    with Locations([(0, 0), (10, 0), (20, 0)]):
        Cylinder(3, 10)   # creates three cylinders
    ```

    ## GridLocations

    ```python
    with GridLocations(x_spacing, y_spacing, x_count, y_count):
        Cylinder(3, 10)
    ```

    ## PolarLocations

    ```python
    with PolarLocations(radius, count):
        Cylinder(3, 10)   # evenly spaced on a circle
    ```
    """)
    return


@app.cell
def _(mo):
    pattern = mo.ui.radio(
        ["Grid", "Polar", "Manual"],
        value="Grid",
        label="Location pattern",
    )
    count   = mo.ui.slider(2, 12, value=4, label="Count")
    spacing = mo.ui.slider(10, 40, value=20, label="Spacing / Radius")
    mo.vstack([pattern, count, spacing])
    return count, pattern, spacing


@app.cell
def _(Align, Box, Cylinder, GridLocations, PolarLocations, Locations, BuildPart, cad, count, pattern, spacing):
    from build123d import BuildPart, Mode

    with BuildPart() as part:
        Box(80, 80, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))
        if pattern.value == "Grid":
            side = max(1, int(count.value ** 0.5))
            with GridLocations(spacing.value, spacing.value, side, side):
                Cylinder(4, 10, mode=Mode.SUBTRACT)
        elif pattern.value == "Polar":
            with PolarLocations(spacing.value, count.value):
                Cylinder(4, 10, mode=Mode.SUBTRACT)
        else:
            with Locations([(0, 0, 8), (20, 0, 8), (-20, 0, 8)]):
                Cylinder(4, 10, mode=Mode.SUBTRACT)

    viewer = cad.Viewer()
    viewer.render(part.part)
    viewer
    return BuildPart, Mode, part, viewer


@app.cell
def _(mo):
    mo.md("""
    ## Exercise

    1. Place 6 cylinders in a hexagonal pattern using `PolarLocations`.
    2. Use `Location((x, y, z), (0, 0, 45))` to rotate a box 45° before
       adding it to the part.
    3. Create a row of holes with varying diameters using a Python `for` loop
       and individual `Location` placements.
    """)
    return


if __name__ == "__main__":
    app.run()
