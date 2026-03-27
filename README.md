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

## Structure

Notebooks are organised by topic:

```
build123d-study/
  01_basics/
  02_sketches/
  03_assemblies/
  ...
```

Each folder contains one or more `.py` marimo notebooks that can be opened and edited directly in the browser.
