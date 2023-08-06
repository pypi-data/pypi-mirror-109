# python-md

python-md is a Python library for helping writing Markdown documents.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install python-md.

```bash
pip install python-md
```

## Usage

```python
from python_md import Markdown


md = Markdown('examples.md')
content = md.h1('simple python-md example')
header = ['this', 'is', 'a', 'table', 'header']
body = [
    ['this', 'is', 'the', 'first', 'row'],
    ['this', 'is', 'the', 'second', 'row'],
    ['this', 'is', 'the', 'third', 'row'],
]
content += md.table(header, body)
md.write_to_file(content, 'w+')
```

For more examples of what you can do, check here:
- Code: [examples.py](examples.py)

You can also use `make` to generate the examples file:
```shell
make examples
```

## Testing
To run tests, use:
```shell
make tests
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](LICENSE)
