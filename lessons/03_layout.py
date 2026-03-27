import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Lesson 03 — Layout

    marimo provides layout helpers to organise UI elements and content within a
    single cell output.

    ## Key helpers

    | Helper | Description |
    |---|---|
    | `mo.vstack([...])` | Stack items vertically |
    | `mo.hstack([...])` | Stack items horizontally |
    | `mo.tabs({...})` | Tabbed container |
    | `mo.accordion({...})` | Collapsible sections |
    | `mo.callout(...)` | Highlighted info/warning box |
    | `mo.stat(...)` | Single metric display |

    Layouts can be nested freely.
    """)
    return


@app.cell
def _(mo):
    width  = mo.ui.slider(10, 200, value=80,  label="Width")
    depth  = mo.ui.depth  = mo.ui.slider(10, 200, value=60, label="Depth")
    height = mo.ui.slider(5,  100, value=30,  label="Height")

    controls = mo.vstack([width, depth, height], gap=1)
    controls
    return depth, height, width


@app.cell
def _(depth, height, mo, width):
    volume = width.value * depth.value * height.value
    area   = 2 * (width.value * depth.value +
                  width.value * height.value +
                  depth.value * height.value)

    stats = mo.hstack([
        mo.stat(value=f"{volume:,} mm³", label="Volume"),
        mo.stat(value=f"{area:,} mm²",  label="Surface area"),
    ])
    stats
    return area, volume


@app.cell
def _(mo):
    mo.tabs({
        "Info":    mo.md("Tabs keep related content together without clutter."),
        "Warning": mo.callout(mo.md("Watch your wall thickness!"), kind="warn"),
        "Tip":     mo.callout(mo.md("Use `mo.hstack` for side-by-side controls."), kind="info"),
    })
    return


@app.cell
def _(mo):
    mo.md("""
    ## Exercise

    1. Wrap the three sliders and the stats row in a single `mo.vstack`.
    2. Add a fourth slider for wall thickness and show it in the stats.
    3. Use `mo.accordion` to hide/show an "Advanced options" section.
    4. Add a `mo.callout` with `kind="danger"` when volume exceeds 1 000 000 mm³.
    """)
    return


if __name__ == "__main__":
    app.run()
