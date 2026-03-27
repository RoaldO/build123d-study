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
    # Lesson 02 — UI Elements

    marimo has a rich set of built-in UI components. Because of reactivity, any
    cell that reads `.value` from a UI element automatically re-runs when the
    user interacts with it — no callbacks needed.

    ## Common elements

    | Element | Description |
    |---|---|
    | `mo.ui.slider` | Numeric range |
    | `mo.ui.number` | Numeric input field |
    | `mo.ui.text` | Text input |
    | `mo.ui.dropdown` | Select from a list |
    | `mo.ui.checkbox` | Boolean toggle |
    | `mo.ui.button` | Trigger an action |
    | `mo.ui.radio` | Pick one from a set |

    Each element has a `.value` property you read in downstream cells.
    """)
    return


@app.cell
def _(mo):
    size = mo.ui.slider(1, 100, value=42, label="Size (mm)")
    size
    return (size,)


@app.cell
def _(mo):
    material = mo.ui.dropdown(
        ["PLA", "PETG", "ABS", "TPU"],
        value="PLA",
        label="Material",
    )
    material
    return (material,)


@app.cell
def _(mo):
    name = mo.ui.text(placeholder="Enter a name", label="Part name")
    name
    return (name,)


@app.cell
def _(material, mo, name, size):
    mo.md(f"""
    **Summary**

    - Part: `{name.value or '—'}`
    - Material: `{material.value}`
    - Size: `{size.value} mm`
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Exercise

    1. Add a `mo.ui.number` element for wall thickness (range 0.4 – 5.0 mm).
    2. Add a `mo.ui.checkbox` labelled "Add support material".
    3. Extend the summary to include both new values.
    4. Try `mo.ui.radio` with options `["Draft", "Normal", "Fine"]` for print quality.
    """)
    return



@app.cell(hide_code=True)
def _(mo):
    import shutil
    from pathlib import Path as _Path

    _name = "02_ui_elements.py"
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
