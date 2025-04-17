# WireVizGUI

## Summary

This project aims to provide a simple and portable graphical interface for [WireViz](https://github.com/formatc1702/WireViz) by embedding [WireViz-Web](https://github.com/jurgen-key/wireviz-web) into a standalone executable. The GUI is implemented using [pywebview](https://github.com/r0x0r/pywebview), ensuring a lightweight native window without requiring a web browser.

**Main goals:**
- Run WireViz through a graphical interface.
- Bundle everything (Python, Flask, WireViz-Web, Graphviz) inside a single standalone `.exe`.
- No external dependencies needed for the user (no Python or pip required).
- Fully offline use.

---

## About WireViz and WireViz-Web

**WireViz** is a tool for easily documenting cables, wiring harnesses, and connector pinouts.  
It takes plain text, YAML-formatted files as input and produces beautiful graphical output (SVG, PNG, etc.) using Graphviz.  
It can also automatically generate a Bill of Materials (BOM) and supports many advanced features.

**WireViz-Web** is a wrapper around WireViz created by Jürgen Key.  
It exposes a REST API through Flask to enable running WireViz over HTTP.  
It also includes support for PlantUML rendering thanks to PlantUML Text Encoding format decoding.

---

## Installation and Build

### Install required packages

```bash
pip install -r requirements.txt
```

(Or manually if preferred:)
```bash
pip install pyinstaller
pip install pywebview
pip install requests
pip install wireviz-web
```

### Build the Standalone Executable

```bash
pyinstaller wirevizgui.spec
```

After successful compilation, your standalone executable will be available in the `dist/` folder.

---

## Cleaning the Development Environment

If you need to completely reset your environment after building:

```bash
pip freeze > installed.txt
pip uninstall -r installed.txt -y
```

⚠️ This will uninstall **all** currently installed pip packages.  
After that, you can reinstall only the needed ones using `requirements.txt`.

---

## Notes

- Make sure `Graphviz` binaries are correctly bundled inside the executable or otherwise available at runtime.
- Make sure the `wireviz_web` package is embedded into your project if you want true offline use.
- If needed, copy missing files manually before building.

---