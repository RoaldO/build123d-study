import marimo

__generated_with = "0.21.1"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    import marimo_cad as cad
    from build123d import Box
    return Box, cad, mo


@app.cell(hide_code=True)
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



@app.cell(hide_code=True)
def _(mo):
    import shutil
    from pathlib import Path as _Path

    _name = "06_cad_viewer.py"
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
    _in_workspace = _Path(str(mo.notebook_location())).name == "workspace"
    mo.md("") if _in_workspace else copy_btn
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
