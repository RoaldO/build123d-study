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
    # Lesson 04 — Markdown and State

    ## Markdown

    `mo.md(...)` renders a markdown string. Use an f-string to embed live values:

    ```python
    mo.md(f"The result is **{value}**")
    ```

    All standard markdown is supported: headings, bold, italic, lists, tables,
    code blocks, and LaTeX math via `$...$` or `$$...$$`.

    ## mo.state

    For values that must change in place (e.g. a counter driven by a button),
    marimo provides `mo.state`:

    ```python
    count, set_count = mo.state(0)
    ```

    - `count()` reads the current value.
    - `set_count(new)` updates it and triggers a re-run.

    ## Conditional output

    Because cell outputs are just Python values you can use `if` expressions:

    ```python
    mo.callout(mo.md("Too big!"), kind="danger") if value > 100 else mo.md("")
    ```
    """)
    return


@app.cell
def _(mo):
    count, set_count = mo.state(0)
    return count, set_count


@app.cell
def _(mo, set_count):
    btn = mo.ui.button(
        label="Click me",
        on_click=lambda _: set_count(lambda n: n + 1),
    )
    btn
    return (btn,)


@app.cell
def _(count, mo):
    mo.md(f"Button has been clicked **{count()}** times.")
    return


@app.cell
def _(mo):
    angle = mo.ui.slider(0, 360, value=45, label="Angle (°)")
    angle
    return (angle,)


@app.cell
def _(angle, mo):
    import math
    rad = math.radians(angle.value)
    mo.md(f"""
    | | Value |
    |---|---|
    | Angle | ${angle.value}°$ |
    | Radians | ${rad:.4f}$ |
    | $\\sin$ | ${math.sin(rad):.4f}$ |
    | $\\cos$ | ${math.cos(rad):.4f}$ |
    """)
    return math, rad


@app.cell
def _(mo):
    mo.md("""
    ## Exercise

    1. Add a reset button that sets the counter back to 0.
    2. Show a `mo.callout` with `kind="success"` once the button has been clicked
       10 or more times.
    3. Use `mo.md` with a LaTeX formula to display the formula for a cylinder's
       volume, with a live result driven by radius and height sliders.
    """)
    return


if __name__ == "__main__":
    app.run()
