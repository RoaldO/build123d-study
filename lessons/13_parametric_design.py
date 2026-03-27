import marimo
import json
from pathlib import Path

try:
    _use_columns = json.loads((Path.home() / ".marimocad_prefs.json").read_text()).get("layout") == "columns"
except Exception:
    _use_columns = False

app = marimo.App(width="full" if _use_columns else "medium")


@app.cell
def _():
    import json
    import marimo as mo
    import marimo_cad as cad
    from pathlib import Path
    from build123d import (
        BuildPart, BuildSketch,
        Cylinder, Rectangle,
        extrude, fillet,
        Align, Axis, PolarLocations,
    )

    try:
        use_columns = json.loads((Path.home() / ".marimocad_prefs.json").read_text()).get("layout") == "columns"
    except Exception:
        use_columns = False

    return Align, Axis, BuildPart, BuildSketch, Cylinder, PolarLocations, Rectangle, cad, extrude, fillet, mo, use_columns


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Lesson 13 — Parametric Design

    This lesson brings everything together. We build a **parametric lid** —
    a rectangular plate with rounded corners, a lip, and polar mounting holes.

    All dimensions are driven by sliders. Every change instantly updates
    the model.

    ## Design parameters

    - Outer dimensions (length, width)
    - Wall thickness
    - Lip height
    - Corner fillet radius
    - Number and radius of mounting holes
    """)
    return


@app.cell
def _(mo):
    length    = mo.ui.slider(40, 200, value=100, step=2,   label="Length (mm)")
    width     = mo.ui.slider(30, 150, value=70,  step=2,   label="Width (mm)")
    thickness = mo.ui.slider(1,  10,  value=3,   step=0.5, label="Thickness (mm)")
    lip_h     = mo.ui.slider(0,  20,  value=5,   step=1,   label="Lip height (mm)")
    fillet_r  = mo.ui.slider(0,  15,  value=5,   step=1,   label="Corner fillet (mm)")
    hole_d    = mo.ui.slider(2,  8,   value=3,   step=0.5, label="Hole diameter (mm)")
    hole_n    = mo.ui.slider(2,  8,   value=4,   step=1,   label="Number of holes")
    hole_ring = mo.ui.slider(10, 60,  value=30,  step=1,   label="Hole ring radius (mm)")
    return fillet_r, hole_d, hole_n, hole_ring, length, lip_h, thickness, width


@app.cell
def _(
    Align, Axis, BuildPart, BuildSketch, Cylinder, PolarLocations, Rectangle,
    cad, extrude, fillet,
    fillet_r, hole_d, hole_n, hole_ring, length, lip_h, mo, thickness, use_columns, width,
):
    from build123d import Mode

    with BuildPart() as lid:
        with BuildSketch():
            Rectangle(length.value, width.value)
        extrude(amount=thickness.value)

        if lip_h.value > 0:
            lip_w = 3.0
            with BuildSketch(lid.faces().sort_by(Axis.Z)[-1]):
                Rectangle(length.value, width.value)
                Rectangle(
                    length.value - 2 * lip_w,
                    width.value  - 2 * lip_w,
                    mode=Mode.SUBTRACT,
                )
            extrude(amount=lip_h.value)

        total_h = thickness.value + lip_h.value
        with PolarLocations(hole_ring.value, int(hole_n.value)):
            Cylinder(hole_d.value / 2, total_h + 1, mode=Mode.SUBTRACT)

        if fillet_r.value > 0:
            try:
                fillet(lid.edges().filter_by(Axis.Z), fillet_r.value)
            except Exception:
                pass

    viewer = cad.Viewer()
    viewer.render(lid.part)

    controls = mo.vstack([length, width, thickness, lip_h, fillet_r, hole_d, hole_n, hole_ring])
    mo.hstack([controls, viewer], widths=[1, 3]) if use_columns else mo.vstack([controls, viewer])
    return Mode, lid, total_h, viewer


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise

    1. Add a chamfer on the top edge ring instead of (or in addition to) the
       vertical fillet.
    2. Add a `mo.ui.checkbox` to toggle the lip on/off.
    3. Add an export button that saves the model as `lid.step` using
       `export_step(lid.part, "lid.step")`.
    4. **Final challenge**: modify the design to be a box with a separate lid.
       Render both as a named dict in the viewer.
    """)
    return



@app.cell(hide_code=True)
def _(mo):
    import shutil
    from pathlib import Path as _Path

    _name = "13_parametric_design.py"
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
