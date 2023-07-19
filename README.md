<br>
<div align="center">
<img src="https://raw.githubusercontent.com/katoss/cardsort/main/logo.png" width="400">
</div>
<hr>

## A Python package to cluster and visualize data from open card sorting tasks

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
![PyPI](https://img.shields.io/pypi/v/cardsort)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/katoss/cardsort/CI.yml)
![Read the Docs](https://img.shields.io/readthedocs/cardsort)
![Python](https://img.shields.io/badge/Python-3.8--3.12-green)
![Codecov](https://img.shields.io/codecov/c/github/katoss/cardsort)


Cardsort helps UX researchers quickly analyse data from open card sorting exercises using hierarchical cluster analysis. This task helps to understand how people organize information, and is frequently used to develop information architectures for websites. Click [here](https://www.nngroup.com/articles/card-sorting-definition/) to learn more about the card sorting method.

__More precisely, cardsort helps you to:__
* Create distance matrices using hierarchical cluster analysis
* Create dendrograms from based on these matrices
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

The data used in this example can be found under [/docs/example-data.csv](https://github.com/katoss/cardsort/blob/main/docs/example-data.csv).

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
  user_id   cluster_label                                              cards
0       2  Healthy snacks                                    [Banana, Apple]
1       3          Snacks     [Sandwich, Croissant, Banana, Mooncake, Apple]
2       4          Fruits                                    [Apple, Banana]
3       5            Food  [Banana, Croissant, Apple, Sandwich, Hot Dog, ...
```
__Interpretation:__ In this case, the users with IDs 2 and 4 made clusters containing exactly the two cards of interest ('Banana' and 'Apple', as specified in the input variable 'cards'). User 2 labelled this cluster 'Healthy snacks', and user 4 'Fruits'. Users 3 and 5 also clustered these cards together, but they included additional other cards in the same cluster, and labelled the cluster 'Snacks' or 'Food'. User 1 does not appear in the output, because they did not cluster the cards together.

### Accepted data
* This package works with data exports from [kardsort.com](https://kardsort.com/) (Export format 'Casolysis Data (.csv) - Recommended') or other data following the same structure.
* __Columns:__ ```card_id, card_label, category_id, category_label, user_id```

### Advanced usage
See [documentation](https://cardsort.readthedocs.io)

## Contributing

Interested in contributing? Check out the [contributing guidelines](https://cardsort.readthedocs.io/en/latest/contributing.html). Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`cardsort` is licensed under the of the [MIT license](https://github.com/katoss/cardsort/blob/documentation/LICENSE).

## Credits

`cardsort` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
