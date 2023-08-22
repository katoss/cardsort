<div align="center">
<img src="https://raw.githubusercontent.com/katoss/cardsort/main/logo.png" width="400">
</div>
<hr>

## A Python package to cluster and visualize data from open card sorting tasks

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[logo]: https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square 'Number of contributors on All-Contributors'
<!-- ALL-CONTRIBUTORS-BADGE:END -->
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
![PyPI](https://img.shields.io/pypi/v/cardsort)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/katoss/cardsort/CI.yml)
![Read the Docs](https://img.shields.io/readthedocs/cardsort)
![Python](https://img.shields.io/badge/Python-3.8--3.12-green)
![Codecov](https://img.shields.io/codecov/c/github/katoss/cardsort)
[![DOI](https://zenodo.org/badge/614836750.svg)](https://zenodo.org/badge/latestdoi/614836750)
[![pyOpenSci](https://tinyurl.com/y22nb8up)](https://github.com/pyOpenSci/software-review/issues/102)
[![All Contributors][logo]](#contributors-)


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

## Project information
### License

`cardsort` is licensed under the of the [MIT license](https://github.com/katoss/cardsort/blob/documentation/LICENSE).

### Contributing

Interested in contributing? Check out the [contributing guidelines](https://cardsort.readthedocs.io/en/latest/contributing.html). Please note that this project is released with a [Code of Conduct](https://github.com/katoss/cardsort/blob/main/CONDUCT.md). By contributing to this project, you agree to abide by its terms.

### Citation

If you want to cite cardsort, please use the following DOI: [![DOI](https://zenodo.org/badge/614836750.svg)](https://zenodo.org/badge/latestdoi/614836750)

### Credits

`cardsort` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

## Contributors

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/katoss"><img src="https://avatars.githubusercontent.com/u/23122159?v=4?s=100" width="100px;" alt="Katharina Kloppenborg"/><br /><sub><b>Katharina Kloppenborg</b></sub></a><br /><a href="https://github.com/katoss/cardsort/commits?author=katoss" title="Code">💻</a> <a href="#ideas-katoss" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/katoss/cardsort/commits?author=katoss" title="Documentation">📖</a> <a href="#design-katoss" title="Design">🎨</a> <a href="#projectManagement-katoss" title="Project Management">📆</a> <a href="#research-katoss" title="Research">🔬</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://tzovar.as"><img src="https://avatars.githubusercontent.com/u/674899?v=4?s=100" width="100px;" alt="Bastian Greshake Tzovaras"/><br /><sub><b>Bastian Greshake Tzovaras</b></sub></a><br /><a href="#fundingFinding-gedankenstuecke" title="Funding Finding">🔍</a> <a href="https://github.com/katoss/cardsort/commits?author=gedankenstuecke" title="Code">💻</a> <a href="#ideas-gedankenstuecke" title="Ideas, Planning, & Feedback">🤔</a> <a href="#mentoring-gedankenstuecke" title="Mentoring">🧑‍🏫</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://batalex.github.io"><img src="https://avatars.githubusercontent.com/u/11004857?v=4?s=100" width="100px;" alt="Alex Batisse"/><br /><sub><b>Alex Batisse</b></sub></a><br /><a href="https://github.com/katoss/cardsort/pulls?q=is%3Apr+reviewed-by%3ABatalex" title="Reviewed Pull Requests">👀</a> <a href="#ideas-Batalex" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.linkedin.com/in/semidan-robaina/"><img src="https://avatars.githubusercontent.com/u/21340147?v=4?s=100" width="100px;" alt="Semidán Robaina"/><br /><sub><b>Semidán Robaina</b></sub></a><br /><a href="https://github.com/katoss/cardsort/pulls?q=is%3Apr+reviewed-by%3ARobaina" title="Reviewed Pull Requests">👀</a> <a href="#ideas-Robaina" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/khynder"><img src="https://avatars.githubusercontent.com/u/133049827?v=4?s=100" width="100px;" alt="khynder"/><br /><sub><b>khynder</b></sub></a><br /><a href="https://github.com/katoss/cardsort/pulls?q=is%3Apr+reviewed-by%3Akhynder" title="Reviewed Pull Requests">👀</a> <a href="#ideas-khynder" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
