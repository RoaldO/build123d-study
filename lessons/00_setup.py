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

    def _save(_):
        _path = Path.home() / ".marimocad_prefs.json"
        _path.write_text(json.dumps({"layout": layout.value}, indent=2))
        return layout.value

    save_btn = mo.ui.button(label="Save preference", on_click=_save)
    mo.vstack([layout, save_btn])
    return layout, save_btn


@app.cell(hide_code=True)
def _(mo, save_btn):
    if save_btn.value:
        mo.callout(
            mo.md(f"Saved **{save_btn.value}** layout.  \n"
                  "Re-open any lesson to apply the new setting."),
            kind="success",
        )
    else:
        mo.md("*Click **Save preference** to write your choice.*")
    return


if __name__ == "__main__":
    app.run()
