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
    # Setup — Screen Layout Preference

    Some lessons display a 3D model next to the controls. On a wide or
    ultrawide screen this works best with a **two-column layout**; on a
    standard screen a single-column layout is more comfortable.

    Your choice is saved to `~/.marimocad_prefs.json` and applied
    automatically whenever you open a lesson. It is not tracked by git.

    ---
    """)
    return


@app.cell
def _(Path, json, mo):
    try:
        _saved = json.loads((Path.home() / ".marimocad_prefs.json").read_text()).get("layout", "medium")
    except Exception:
        _saved = "medium"
    layout = mo.ui.radio(
        options={"medium — single column (default)": "medium",
                 "columns — controls left, model right": "columns"},
        value=_saved,
        label="Preferred layout",
    )
    layout
    return (layout,)


@app.cell
def _(mo):
    save_btn = mo.ui.button(label="Save preference")
    save_btn
    return (save_btn,)


@app.cell
def _(Path, json, layout, mo, save_btn):
    if save_btn.value:
        _path = Path.home() / ".marimocad_prefs.json"
        _path.write_text(json.dumps({"layout": layout.value}, indent=2))
        mo.callout(
            mo.md(f"Saved **{layout.value}** layout to `{_path}`.  \n"
                  "Re-open any lesson to apply the new setting."),
            kind="success",
        )
    else:
        mo.md("*Click **Save preference** to write your choice.*")
    return


if __name__ == "__main__":
    app.run()
