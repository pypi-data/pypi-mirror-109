# color_palette_at

color_palette_at is a Python library that returns a list of most often occuring colors in the given image.  
You can define number of colors and color values format that will be returned.  
Currently supported formats:  
hex

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install color_palette_at:

```bash
pip install color_palette_at
```

## Usage

```python
from color_palette_at import ColorPalette

print(ColorPalette('path/to/an/image.jpg', 5, 'hex'))
# Expected result:
# ['#e0bb1e', '#c79121', '#b37027', '#ba6432', '#851f16']
```

## Tests
You will need a [pytest](https://pypi.org/project/pytest/) library to run tests. After installation of said module, run this command in a directory where the color_palette_at library is located:
```
pytest
```
To run all the tests.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)