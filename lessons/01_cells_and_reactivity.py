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
    return


if __name__ == "__main__":
    app.run()
