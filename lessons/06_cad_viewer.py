import marimo

__generated_with = "0.21.1"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    import marimo_cad as cad
    from build123d import Box
    return Box, cad, mo


@app.cell
def _(mo):
    mo.md("""
    # Lesson 06 — The CAD Viewer

    ## marimo-cad Viewer

    `cad.Viewer()` is the 3D viewport for your models. Key properties:

    - **Renders any build123d `Shape`** — solids, shells, compounds.
    - **Stable camera** — re-rendering after a parameter change does *not*
      reset the viewpoint.
    - **Named parts** — pass a dict to render a multi-part assembly with
      each part in its own colour.
    - **Export** — the viewer toolbar has buttons for STL, STEP, and glTF.

    ## Basic usage

    ```python
    viewer = cad.Viewer()
    viewer.render(my_shape)
    viewer          # return the viewer to display it
    ```

    ## Multi-part

    ```python
    viewer.render({"base": base_part, "lid": lid_part})
    ```

    ## Placing controls next to the viewer

    Use `app = marimo.App(width="columns")` and set `column=` on your cells
    to place sliders in column 0 and the viewer in column 1.
    """)
    return


@app.cell(column=0)
def _(mo):
    w = mo.ui.slider(10, 150, value=60, label="Width")
    d = mo.ui.slider(10, 150, value=40, label="Depth")
    h = mo.ui.slider(5,  80,  value=20, label="Height")
    mo.vstack([w, d, h])
    return d, h, w


@app.cell(column=1)
def _(Box, cad, d, h, w):
    box     = Box(w.value, d.value, h.value)
    viewer  = cad.Viewer()
    viewer.render(box)
    viewer
    return box, viewer


@app.cell(column=0)
def _(mo):
    mo.md("""
    ## Exercise

    1. Add a fourth slider for a second box and render both as a named dict:
       `{"box_a": ..., "box_b": ...}`.
    2. Use the export button in the toolbar to download the model as STL.
    3. Try `app = marimo.App(width="medium")` instead of `"columns"` — what
       changes?
    """)
    return


if __name__ == "__main__":
    app.run()
