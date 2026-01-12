# PythoShop

PythoShop is a Python-based image editing application supporting image manipulation through a graphical interface. The program uses BMP images and includes a collection of filters and tools implemented in Python. The application uses Kivy for the user interface and separates image-processing logic from UI code for clarity and organization.

---

## Functionality

PythoShop provides both image-wide filters and interactive tools.

### Filters

Filters apply to the entire image and include:

- Color channel removal and maximization
- Color inversion
- Grayscale and partial grayscale effects
- Brightness adjustment
- Posterization (two-tone and four-tone)
- Static effects
- Color remapping effects
- Channel swapping
- Vertical fade effects
- Image blending and chroma key overlays

All filters are registered using decorators and automatically loaded into the interface.

---

### Tools

Tools require user interaction and apply effects at specific locations:

- Drawing horizontal and vertical lines
- Drawing centered lines
- Changing individual pixels
- Marking the center pixel
- Drawing image borders
- Selecting pixel coordinates
- Sampling colors from the image

Tools are also registered using decorators and are selectable from the interface.

---

## User Interface

The interface is built with Kivy and supports:

- Two image tabs (primary and secondary)
- Loading images from disk or via drag-and-drop
- A color picker for selecting RGB values
- Tool and filter selection via dropdown menus
- Pixel-accurate rendering
- Saving edited images as BMP files

---

## Requirements

- Python 3.x
- kivy
- pillow

---

## Running the Application

```bash
python main.py
