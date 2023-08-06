# .bdf to NumPy

This project takes a .bdf file and turns it into a [NumPy](https://www.numpy.org/) Array with an intended use with LED matrix displays. My [LED Stock Ticker](https://gitlab.com/them-boys/raspberry-pi-stock-ticker) uses this package. A good list of .bdf files can be found [here](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/fonts)

## Usage

```python
from bdfparse import Font

font = Font('9x18.bdf')

print(font.word('Hi'))
```

Which outputs:

```python
[[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 1 0 0 0 0 0 1 0 0 0 0 1 1 0 0 0]
 [0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0]
 [0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0]
 [0 0 1 0 0 0 0 0 1 0 0 0 1 1 1 0 0 0]
 [0 0 1 1 1 1 1 1 1 0 0 0 0 0 1 0 0 0]
 [0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0]
 [0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0]
 [0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0]
 [0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0]
 [0 0 1 0 0 0 0 0 1 0 0 0 1 1 1 1 1 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]]
```

Or you can use matplotlib to make the output a bit prettier.

```python
import matplotlib.pyplot as plt

plt.imshow(font.word('Anson'))
```

![Example of code output that reads Anson.](example.png)
