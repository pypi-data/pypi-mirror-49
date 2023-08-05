# mpl_colors

A python 3.6+ library extending matplotlib's color handling.

## Named color enums

Makes matplotlib's [named colors](https://matplotlib.org/examples/color/named_colors.html) more discoverable.

Defines enums for each of matplotlib's sets of named colours (base, Tableau, xkcd and CSS4), and one which combines all of them (where Tableau and xkcd names are prepended with `TAB_` and `XKCD_` respectively, like matplotlib).
Color names are in `SCREAMING_SNAKE_CASE`, as recommended.
Names originally containing a slash (`/`) replace it with the `_SLASH_` (necessary to prevent collisions).

Instances of these enums are also instances of a named tuple with members `r`, `g`, and `b` (all floats between 0 and 1).
They also support a number of methods for conversion into `colour.Color` objects, and RGBA, HSL, HSV, and YIQ tuples.
Also, length-6 hex strings (prepended with `#`) and `colour`'s "web" format (whichever is shortest of W3C named color, length-3 hex, or length-6 hex, preferring named as a tie-break).

The enums are automatically generated directly from `matplotlib.colors` using the included `make_colors.py`.
Like matplotlib, they support both spellings of the word "grey"/"gray".

## LabelColormap

`matplotlib.colors.Colormap` subclass which deterministically converts integers into a random RGB tuple.

```python
from matplotlib import pyplot as plt
import numpy as np

from mpl_colors import LabelColorMap

img = np.random.randint(0, 255, (20, 20), dtype=np.uint8)
masked = np.ma.masked_where(img < 100, img)

fig, ax = plt.subplots()
ax.imshow(masked, cmap=LabelColorMap(), interpolation='nearest')
fig.show()
```
