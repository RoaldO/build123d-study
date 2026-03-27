import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import json
    from pathlib import Path

    return Path, json, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Setup

    Run this notebook once before starting the lessons. It does two things:

    1. **Layout preference** — choose single-column or two-column layout.
    2. **Copy lessons to workspace** — copies all lesson files to the
       `workspace/` folder so your edits stay separate from the templates.

    ---

    ## Step 1 — Screen Layout Preference

    Some lessons display a 3D model next to the controls. On a wide or
    ultrawide screen this works best with a **two-column layout**; on a
    standard screen a single-column layout is more comfortable.

    Your choice is saved to `~/.marimocad_prefs.json` and applied
    automatically whenever you open a lesson. It is not tracked by git.
    """)
    return


@app.cell(hide_code=True)
def _(Path, json, mo):
    try:
        _saved = json.loads((Path.home() / ".marimocad_prefs.json").read_text()).get("layout", "medium")
    except Exception:
        _saved = "medium"
    _options = {
        "medium — single column (default)": "medium",
        "columns — controls left, model right": "columns",
    }
    _saved_key = next((k for k, v in _options.items() if v == _saved), "medium — single column (default)")
    layout = mo.ui.radio(options=_options, value=_saved_key, label="Preferred layout")
    layout
    return (layout,)


@app.cell(hide_code=True)
def _(mo):
    save_btn = mo.ui.button(
        label="Save preference",
        value=0,
        on_click=lambda v: v + 1,
        kind="success",
    )
    save_btn
    return (save_btn,)


@app.cell(hide_code=True)
def _(Path, json, layout, mo, save_btn):
    if save_btn.value > 0:
        _path = Path.home() / ".marimocad_prefs.json"
        _path.write_text(json.dumps({"layout": layout.value}, indent=2))
        _out = mo.callout(
            mo.md(f"Saved **{layout.value}** layout.  \n"
                  "Re-open any lesson to apply the new setting."),
            kind="success",
        )
    else:
        _out = mo.md("*Click **Save preference** to write your choice.*")
    _out


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    ## Step 2 — Copy lessons to workspace

    The `workspace/` folder is gitignored — your edits and progress stay local.
    Click the button below to copy all lesson templates there.

    > **Note:** existing files in `workspace/` will be overwritten.
    """)
    return


@app.cell(hide_code=True)
def _(Path, mo):
    import shutil

    def _do_copy(v):
        _lessons = Path(str(mo.notebook_location()))
        _workspace = _lessons.parent / "workspace"
        _workspace.mkdir(exist_ok=True)
        _copied = []
        for _f in sorted(_lessons.glob("[0-9][0-9]_*.py")):
            shutil.copy2(_f, _workspace / _f.name)
            _copied.append(_f.name)
        return _copied

    copy_all_btn = mo.ui.button(
        label="Copy all lessons to workspace",
        on_click=_do_copy,
        value=[],
        kind="success",
    )
    copy_all_btn
    return copy_all_btn, shutil


@app.cell(hide_code=True)
def _(Path, copy_all_btn, mo):
    if copy_all_btn.value:
        import os
        _cwd = Path(os.getcwd())
        _first_file = Path(str(mo.notebook_location())).parent / "workspace" / "01_cells_and_reactivity.py"
        _url = "/?file=" + str(_first_file.relative_to(_cwd))
        _out = mo.callout(
            mo.md(
                f"Copied {len(copy_all_btn.value)} lessons to `workspace/`.  \n\n"
                f"[**Start lesson 01 →**]({_url})"
            ),
            kind="success",
        )
    else:
        _out = mo.md("")
    _out


if __name__ == "__main__":
    app.run()
