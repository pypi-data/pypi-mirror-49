# PyRgbPalette
calculate the RGB values for rainbow or shades of red palette 

## Installation
Run the following to install:
```python
pip install pyrgbpalette
```

## Usage
```python
from rgbpalette import rgb_in_rainbow, rgb_in_palette
# generate rgb value
rgb_value = rgb_in_rainbow(0.5)

# generate rgb palette (default: rainbow values)
rgb_value = rgb_in_palette(0.5)

# generate rgb palette as shades of red
rgb_value = rgb_in_palette(0.5, rainbowDisplay=False)
```

# Developing PyRgbPalette
To install pyrgbpalette, along with the tools you
need to develop and run tests, run the following
in your virtualenv:
```bash
$ pip install -e .[dev]


