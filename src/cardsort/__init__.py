# read version from installed package
from importlib.metadata import version
__version__ = version("cardsort")

# import functions into top module namespace
from .analysis import create_dendrogram, get_distance_matrix, get_cluster_labels, get_cluster_labels_df