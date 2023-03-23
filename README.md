# Cardsort analysis

A package that helps UX researchers quickly analyse data from cardsorting exercises.

__Accepted data__
* This package works with data exports from [kardsort.com](https://kardsort.com/) (Export format 'Casolysis Data (.csv) - Recommended')
* This data equals the following structure: ```card_id, card_label, category_id, category_label, user_id```

## Installation

```bash
$ pip install cardsort
```

## Usage

`cardsort` can be used to create dendrograms and extract user-generated category-labels:

```python
from cardsort import analysis
import pandas as pd

path = "example-data.csv" # data with columns: card_id, card_label, category_id, category_label, user_id
df = pd.read_csv(path) 

# create a dendrogram that summarized user-generated clusters
analysis.create_dendrogram(df)

# learn which category labels users gave to clusters
cards = ['Banana', 'Apple']
analysis.get_cluster_labels(df, cards)
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`cardsort` was created by Katharina Kloppenborg and is licensed under the terms of the MIT license.

## Credits

`cardsort` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
