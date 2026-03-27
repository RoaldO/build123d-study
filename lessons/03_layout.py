import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    import os as _os
    from pathlib import Path as _P
    _d = _P(str(mo.notebook_location()))
    _r = _P(_os.getcwd())
    _prev = f"/?file={(_d / '02_ui_elements.py').relative_to(_r)}"
    _next = f"/?file={(_d / '04_markdown_and_state.py').relative_to(_r)}"
    mo.md(f"""
    <small>[← 02]({_prev}) &nbsp;·&nbsp; [04 →]({_next})</small>

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

    ## Column layout

    For wider notebooks — especially useful when working with 3D models — marimo
    supports a two-column layout. Enable it at the top of the file:

    ```python
    app = marimo.App(width="columns")
    ```

    Then assign cells to a column with the `column=` parameter:

    ```python
    @app.cell(column=0)
    def _(mo):
        slider = mo.ui.slider(...)   # controls on the left

    @app.cell(column=1)
    def _(slider):
        viewer.render(...)           # 3D model on the right
        viewer
    ```

    This is particularly handy for CAD work: you keep the 3D model in view
    while tweaking parameters. Lesson 06 shows it in practice.
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


@app.cell(hide_code=True)
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
