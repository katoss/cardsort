# Cardsort analysis

A package that helps UX researchers quickly analyse data from cardsorting exercises.

__More precisely, it helps you to:__
* Create dendrograms
* Extract user-generated category-labels
* Using data exports from [kardsort.com](https://kardsort.com/)

## Table of Contents

- [Documentation](#documentation)
- [Quick start](#quick-start)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Accepted data](#accepted-data)
  - [Advanced usage](#advanced-usage)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

## Documentation
[cardsort.readthedocs.io](https://cardsort.readthedocs.io)

## Quick start
### Installation

```bash
$ pip install cardsort
```

### Usage

`cardsort` can be used to create dendrograms and extract user-generated category-labels:

```python
from cardsort import analysis
import pandas as pd

path = "example-data.csv" # data with columns: card_id, card_label, category_id, category_label, user_id
df = pd.read_csv(path) 
```
__Create a dendrogram that summarizes user-generated clusters__
```python
analysis.create_dendrogram(df)
```

__Output__

![Dendrogram plot generated from example data](https://github.com/katoss/cardsort/blob/main/docs/dendrogram.png?raw=true)

__Learn which category labels users gave to clusters__
```python
cards = ['Banana', 'Apple']
analysis.get_cluster_labels(df, cards)
```
__Output__
```python
['Healthy snacks', 'Snacks', 'Fruits', 'Food']
```

### Accepted data
* This package works with data exports from [kardsort.com](https://kardsort.com/) (Export format 'Casolysis Data (.csv) - Recommended')
* This data equals the following structure: ```card_id, card_label, category_id, category_label, user_id```

### Advanced usage
See [documentation](https://cardsort.readthedocs.io)

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`cardsort` was created by Katharina Kloppenborg and is licensed under the terms of the MIT license.

## Credits

`cardsort` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
