# MyKad

A Python package to check if a MyKad number is valid and gets information such as the birthdate, state of birth, etc.

## The `MyKad` class

```python
from mykad.mykad import MyKad

mykad = MyKad(MYKAD_NUMBER)
```

The following methods are included in the `MyKad` class:

| Method            | Comment                                                      | Example return value |
|-------------------|--------------------------------------------------------------|----------------------|
| `get_unformatted` | Gets the unformatted MyKad string.                           | `'990111431234'`     |
| `get_formatted`   | Gets the formatted MyKad string.                             | `'990111-43-1234'`   |
| `get_birth_year`  | Gets the birthyear of the MyKad holder.                      | `1999`               |
| `get_birth_month` | Gets the birth month (in English) of the MyKad holder.       | `'January'`          |
| `get_birth_day`   | <small>Honestly forgot about this...</small>Will be in 0.0.4 | -                    |
| `is_male`         | Checks if the MyKad holder is a male.                        | `False`              |
| `is_female`       | Checks if the MyKad holder is a female.                      | `True`               |
| `get_gender`      | Gets the gender of the MyKad holder.                         | `'Female'`           |

## Included utility functions

The following utility functions are included under `mykad.utils`:

| Method            | Comment                                                      | Example return value |
|-------------------|--------------------------------------------------------------|----------------------|
| `is_mykad_valid`  | Checks if a MyKad is valid.                                  | `False`              |
