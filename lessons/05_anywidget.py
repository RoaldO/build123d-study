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
    # Lesson 05 — anywidget

    ## What is anywidget?

    [anywidget](https://anywidget.dev) is a lightweight framework for building
    custom interactive widgets with JavaScript. It works in both Jupyter and
    marimo without any extra configuration.

    The key idea: a widget is a Python class that carries some JavaScript. The
    Python side and JS side share **state** through typed attributes called
    *traits*. When a trait changes on either side, the other side is notified
    automatically.

    ## How it works in marimo

    In marimo, anywidgets behave like any other UI element:

    - Render the widget by returning it from a cell.
    - Read its current value via `.value` (or any other trait you defined).
    - Downstream cells react when the widget state changes.

    ## The marimo-cad Viewer

    `marimo-cad` ships a ready-made anywidget called `Viewer`. It renders
    build123d / OCP geometry using `three-cad-viewer` (Three.js based) and
    keeps the camera position stable between re-renders.

    You will use it in depth in the build123d lessons. This lesson focuses on
    understanding *why* it works the way it does.

    ## A minimal custom anywidget

    ```python
    import anywidget
    import traitlets

    class CounterWidget(anywidget.AnyWidget):
        _esm = \"\"\"
        function render({ model, el }) {
            let count = () => model.get("value");
            let btn = document.createElement("button");
            btn.innerHTML = `clicks: ${count()}`;
            btn.addEventListener("click", () => {
                model.set("value", count() + 1);
                model.save_changes();
            });
            model.on("change:value", () => { btn.innerHTML = `clicks: ${count()}`; });
            el.appendChild(btn);
        }
        export default { render };
        \"\"\"
        value = traitlets.Int(0).tag(sync=True)

    counter = CounterWidget()
    counter
    ```

    You don't need to write custom widgets for CAD work — but knowing the
    pattern helps you understand how `marimo-cad` communicates with its viewer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise

    1. Copy the `CounterWidget` snippet above into your workspace notebook and
       run it. Verify that clicking the button updates `counter.value` reactively.
    2. Add a second cell that shows `mo.md(f"Count: {counter.value}")` — does it
       update live?
    3. Read the [anywidget docs](https://anywidget.dev/en/getting-started/) and
       find out what `model.save_changes()` does and why it is needed.
    """)
    return



@app.cell(hide_code=True)
def _(mo):
    import shutil
    from pathlib import Path as _Path

    _name = "05_anywidget.py"
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
