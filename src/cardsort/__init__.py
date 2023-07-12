import logging
from importlib.metadata import version  # read version from installed package
from .analysis import (  # import functions into top module namespace
    create_dendrogram,
    get_distance_matrix,
    get_cluster_labels,
)

__version__ = version("cardsort")
logging.getLogger(__name__).addHandler(logging.NullHandler())
