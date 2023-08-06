# Table Generator

Python package for generating html code for tables from csv files.

## Installation

### Install Using git

*If you wish to run this file from the command line I suggest you use the scripts from the repo at <https://github.com/lol-cubes/table-generator>*

```bash
git clone https://github.com/lol-cubes/table_generator.git
```

### Installl Using pip

```pip
pip install table_generator
```

## Usage:

### generate_html

Args:

`file` (str) - path to file containing csv table

`complete_file` (bool) -  whether or not to add html elements to make code function as a separate file

`header` (bool) - whether or not to turn first row of csv values into `<th>` tags

`pretty` (bool) - whether or not to prettify the output code

`attrs` (dict) - html attributes mapped to corresponding values

Example usage:
```python
from table_generator import generate_html

html_table = generate_html('data.csv', False, True, True, True, 
                           {"class": "table", "id": "data-table"})
```