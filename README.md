# build123d-study

A self-study project for learning parametric CAD modelling with [build123d](https://github.com/gumyr/build123d) and [marimo](https://marimo.io), using interactive notebooks with live 3D previews.

## Running this project

This project is designed to run inside [marimocad](https://github.com/RoaldO/marimocad) — a Dockerised marimo environment with build123d and marimo-cad pre-installed.

### Setup

1. Clone and start marimocad:

   ```bash
   git clone https://github.com/RoaldO/marimocad.git
   cd marimocad
   ```

2. Clone this study project into the `notebooks/` folder:

   ```bash
   cd notebooks/
   git clone https://github.com/RoaldO/build123d-study.git
   ```

3. Start the environment:

   ```bash
   cd ..
   docker compose up
   ```

4. Open [http://localhost:8080](http://localhost:8080) — the `build123d-study/` folder will be visible in the marimo file browser.

### First time setup

If you haven't built the marimocad image yet, use:

```bash
docker compose up --build
```

## Curriculum

| # | File | Topic |
|---|---|---|
| 00 | `00_setup.py` | **Start here** — choose your screen layout preference |
| 01 | `01_cells_and_reactivity.py` | Marimo cells, the reactive execution model |
| 02 | `02_ui_elements.py` | Sliders, dropdowns, text input, buttons |
| 03 | `03_layout.py` | vstack, hstack, tabs, callouts |
| 04 | `04_markdown_and_state.py` | Markdown, LaTeX, mo.state |
| 05 | `05_anywidget.py` | What anywidget is and how it works |
| 06 | `06_cad_viewer.py` | The marimo-cad Viewer widget |
| 07 | `07_primitives.py` | Box, Cylinder, Sphere, Cone, Torus |
| 08 | `08_boolean_operations.py` | Union, subtraction, intersection |
| 09 | `09_sketches.py` | BuildSketch, extrude, revolve |
| 10 | `10_locations.py` | Location, GridLocations, PolarLocations |
| 11 | `11_selectors.py` | edges(), faces(), filter_by(), sort_by() |
| 12 | `12_fillets_and_chamfers.py` | fillet and chamfer on selected edges |
| 13 | `13_parametric_design.py` | Full parametric design — putting it all together |

## Working on lessons

Lesson files in `lessons/` are read-only templates tracked by git. Copy a lesson
to `workspace/` before editing so your progress stays local:

```bash
cp lessons/01_cells_and_reactivity.py workspace/
```

The `workspace/` folder is gitignored — your edits and exported files (STL, STEP)
will never be committed. This also means others can use the same lessons without
any merge conflicts.
