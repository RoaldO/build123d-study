import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Lesson 01 — Cells and Reactivity

    ## What is marimo?

    marimo is a **reactive** Python notebook. Unlike Jupyter, every notebook is a
    plain `.py` file. Cells are Python functions — not a sequence of imperative
    blocks.

    ## How reactivity works

    marimo builds a **dependency graph** from your cells. When a cell changes,
    every cell that depends on it re-runs automatically.

    ```
    cell A  →  cell B  →  cell C
    ```

    If you change `cell A`, both `B` and `C` re-run. You can never have a
    "stale" output.

    ## Rules

    - A cell **returns** the names it wants to share with other cells.
    - A cell **receives** names from other cells as function arguments.
    - Circular dependencies are not allowed.

    ---

    *Read the cells below, then complete the exercises in your workspace copy.*
    """)
    return


@app.cell
def _():
    # This cell defines `greeting`. Other cells can use it.
    greeting = "Hello, marimo!"
    return (greeting,)


@app.cell
def _(greeting):
    # This cell depends on `greeting`. It re-runs when greeting changes.
    loud = greeting.upper()
    return (loud,)


@app.cell
def _(loud):
    print(loud)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise

    Copy this file to your `workspace/` folder and open it there.

    1. Change the value of `greeting` and observe which cells re-run.
    2. Add a fourth cell that counts the number of characters in `loud`.
    3. Try creating a circular dependency — what does marimo do?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    import shutil
    from pathlib import Path as _Path

    _name = "01_cells_and_reactivity.py"
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
    return


if __name__ == "__main__":
    app.run()
