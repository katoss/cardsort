import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform
from typing import List, Union

__all__ = [
    "get_distance_matrix",
    "create_dendrogram",
    "get_cluster_labels",
    "get_cluster_labels_df",
]


logger = logging.getLogger(__name__)


def _check_data(df: pd.DataFrame) -> bool:
    """
    Check if input data is in the correct format.

    Parameters
    ----------
    df : pandas.DataFrame
        Columns:
            Name: card_id, dtype: int64
            Name: card_label, dtype: object
            Name: category_id, dtype: int64
            Name: category_label, dtype: object
            Name: user_id, dtype: int64
        These columns correspond to the 'Casolysis Data (.csv) - Recommended' export from kardsort.com.

    Returns
    -------
    out : bool
        True if the input data is in the correct format, False otherwise.
    """
    # check if first user_id is 1
    if df["user_id"].unique()[0] != 1:
        logger.error("First user_id does not equal 1.")
        return False
    # check if each card_id is always associated with exactly one card_label
    card_id_counts = df.groupby("card_id")["card_label"].nunique()
    for card_id, count in card_id_counts.items():
        if count != 1:
            logger.error(
                f"Card_id {card_id} is associated with {count} different card_labels."
            )
            return False
    # check if all users categorize each card exactly once
    counts = df.groupby(["user_id", "card_id"]).size()
    if (counts > 1).any():
        logger.error("At least one user categorized at least one card more than once.")
        return False
    n_cards = df["card_id"].nunique()
    n_users = df["user_id"].nunique()
    expected_size = n_cards * n_users
    if len(counts) != expected_size:
        logger.error("At least one user does not categorized at least one card.")
        return False
    return True


def _get_distance_matrix_for_user(df_user: pd.DataFrame) -> np.ndarray:
    """
    Return distance matrix for an individual user.

    Parameters
    ----------
    df : pandas.DataFrame (subset for a single user_id)
        Columns:
            Name: card_id, dtype: int64
            Name: card_label, dtype: object
            Name: category_id, dtype: int64
            Name: category_label, dtype: object
            Name: user_id, dtype: int64
        These columns correspond to the 'Casolysis Data (.csv) - Recommended' export from kardsort.com.

    Returns
    -------
    out : np.ndarray
        A distance matrix representing the pairwise similarity of all cards for an individual user (1 if
        they put two cards together, 0 otherwise).
    """
    df_user = df_user.sort_values("card_id")
    arr = df_user["category_label"].values
    X = (arr != arr[:, None]).astype(float)
    return X


def get_distance_matrix(df: pd.DataFrame) -> np.ndarray:
    """
    Return condensed distance matrix from kardsort data.

    Parameters
    ----------
    df : pandas.DataFrame
        Columns:
            Name: card_id, dtype: int64
            Name: card_label, dtype: object
            Name: category_id, dtype: int64
            Name: category_label, dtype: object
            Name: user_id, dtype: int64
        These columns correspond to the 'Casolysis Data (.csv) - Recommended' export from kardsort.com.

    Returns
    -------
    out : ndarray
        A condensed distance matrix (a flat array containing the upper triangle of a distance matrix)
        representing the pairwise similarity of all cards.
    """
    if _check_data(df) == False:
        logger.error(
            "The DataFrame does not correspond to the required format. No distance matrix generated."
        )
        return None
    else:
        user_ids = df["user_id"].unique()
        for id_ in user_ids:
            df_u = df.loc[df["user_id"] == id_]
            logger.info(f"Computing distance matrix for user {id_}")
            distance_matrix_user = _get_distance_matrix_for_user(df_u)
            if id_ == 1:
                distance_matrix_all = distance_matrix_user
            else:
                distance_matrix_all = np.add(distance_matrix_all, distance_matrix_user)
        condensed_distance_matrix = squareform(distance_matrix_all)
        return condensed_distance_matrix


def create_dendrogram(
    df, distance_matrix=None, count="fraction", linkage="average", color_threshold=None
) -> None:
    """
    Plot hierarchical clustering of kardsort data as dendrogram.

    Parameters
    ----------
    df : pandas.DataFrame
        Columns:
            Name: card_id, dtype: int64
            Name: card_label, dtype: object
            Name: category_id, dtype: int64
            Name: category_label, dtype: object
            Name: user_id, dtype: int64
        These columns correspond to the 'Casolysis Data (.csv) - Recommended' export from kardsort.com.
        The dataframe is used to extract leaf labels, and, if no distance_matrix provided, to calculate the distance matrix.

    distance_matrix : ndarray, optional
        Takes a condensed distance matrix as input: A flat array containing the upper triangular of the distance matrix.
        A pre-calculated condensed distance matrix can be provided to save time generating the dendrogram.
        If not specified, a new distance matrix will be calculated from df.

    count : str, optional
        How similarity is displayed.

        'fraction'
        Similarity is displayed as a fraction between 0 and 1.

        'absolute'
        Similarity is displayed as absolute counts from 0 to n = number of users.

    linkage : str, optional
        Linkage method used to compute the distance between two clusters.

        'average'
        Unweighted average distance between all elements in the clusters (UPGMA).

        'complete'
        Distance between the elements that are the farthest away from each other in the two clusters.

        'single'
        Distance between the elements that are the closest each other in the two clusters.

    color_threshold : double, optional
        Level below which to cut the color threshold in the dendrogram branches.
        Can be a fraction (0 - 1) or an absolute value (<= n = number of users).
        The default cut is at 75%.
    """
    if _check_data(df) == False:
        logger.error(
            "The DataFrame does not correspond to the required format. No dendrogram generated."
        )
        return None
    else:
        if distance_matrix is None:
            distance_matrix = get_distance_matrix(df)

        count_types = ["absolute", "fraction"]
        if count not in count_types:
            raise ValueError("Invalid count type. Expected one of: %s" % count_types)

        linkage_types = ["average", "complete", "single"]
        if linkage not in linkage_types:
            raise ValueError("Invalid linkage. Expected one of: %s" % linkage_types)

        if count == "fraction":
            distance_matrix = distance_matrix / np.max(distance_matrix)
            color_threshold = 0.75 if color_threshold is None else color_threshold
        else:
            color_threshold = (
                np.max(distance_matrix) * 0.75
                if color_threshold is None
                else color_threshold
            )

        Z = hierarchy.linkage(distance_matrix, linkage)
        plt.figure(layout="constrained")
        labels = (
            df.loc[df["user_id"] == 1]
            .sort_values("card_id")["card_label"]
            .squeeze()
            .to_list()
        )
        dn = hierarchy.dendrogram(
            Z, labels=labels, orientation="right", color_threshold=color_threshold
        )

        x_max = np.max(distance_matrix)
        plt.xticks(
            np.arange(0.0, 1.1, 0.1) if x_max <= 1 else np.arange(0, x_max + 1, 1)
        )

        for leaf, leaf_color in zip(
            plt.gca().get_yticklabels(), dn["leaves_color_list"]
        ):
            leaf.set_color(leaf_color)
        plt.show()


def _get_cluster_label_for_user(
    df_u: pd.DataFrame, cluster_cards: List[str]
) -> Union[str, None]:
    """
    Return labels an individual user created for clusters including a given list of cards.

    Parameters
    ----------
    df : pandas.DataFrame (subset for a single user_id)
        Columns:
                Name: card_id, dtype: int64
                Name: card_label, dtype: object
                Name: category_id, dtype: int64
                Name: category_label, dtype: object
                Name: user_id, dtype: int64
        These columns correspond to the 'Casolysis Data (.csv) - Recommended' export from kardsort.com.

    cluster_cards : list of str
        List of card-labels for which you would like to get user-generated cluster-labels.

    Returns
    -------
    out : str
        Category_label for the list of card_labels provided (if all cards have the same label).
    OR
    out : None
        If the cards in the list provided do not have the same card_label.
    """
    list_cat = df_u.loc[
        df_u["card_label"].isin(cluster_cards), "category_label"
    ].unique()
    if len(list_cat) == 1:
        return list_cat.squeeze().tolist()
    else:
        return None


def _get_cards_for_label(cluster_label: str, df_u: pd.DataFrame) -> List[str]:
    """
    Return list of all cards with a given cluster label for an individual user.

    Parameters
    ----------
    cluster_label : str
        A category label
    df_u : pandas.DataFrame (subset for an individual user_id)
        Columns:
                Name: card_id, dtype: int64
                Name: card_label, dtype: object
                Name: category_id, dtype: int64
                Name: category_label, dtype: object
                Name: user_id, dtype: int64
        These columns correspond to the 'Casolysis Data (.csv) - Recommended' export from kardsort.com.

    Returns
    -------
    out : List of str
        List including all card_labels that have the given category_label
    """
    cards_list = df_u.loc[
        df_u["category_label"] == cluster_label, "card_label"
    ].tolist()
    return cards_list


def get_cluster_labels(
    df: pd.DataFrame,
    cluster_cards: List[str],
    print_results: bool = True,
    return_df_results: bool = True,
) -> Union[pd.DataFrame, None]:
    """
    Return labels users created for clusters including a given list of cards.

    Parameters
    ----------
    df : pandas.DataFrame
        Columns:
                Name: card_id, dtype: int64
                Name: card_label, dtype: object
                Name: category_id, dtype: int64
                Name: category_label, dtype: object
                Name: user_id, dtype: int64
        These columns correspond to the 'Casolysis Data (.csv) - Recommended' export from kardsort.com.

    cluster_cards : list of str
        List of card-labels for which you would like to get user-generated cluster-labels.

    print_results : bool, optional
        If true, prints which users grouped cards together and under which label

    return_df_results: bool, optional
       If true, returns a dataframe with results

    Returns
    -------
    out : pandas.DataFrame (default)
        Columns:
            Name: user_id, int
            Name: cluster_label, str
            Name: cards, list of str
        Dataframe with one row for each user who clustered the given cards together, including category label and
        the full list of cards in that category.
    OR
    out : None
        If return_df_results = False
    """
    if _check_data(df) == False:
        logger.error(
            "The data does not correspond to the required format. No cluster labels extracted."
        )
        return None
    else:
        if not set(cluster_cards) <= set(df["card_label"]):
            missing_card_labels = set(cluster_cards) - set(df["card_label"])
            logger.info(
                f'"{missing_card_labels}" is/are not a valid card label. Removed from list.'
            )
            cluster_cards = [
                card_label
                for card_label in cluster_cards
                if card_label not in missing_card_labels
            ]
            if len(cluster_cards) > 0:
                logger.info("Continue with cards: %s" % cluster_cards)
            else:
                logger.info("No cards left in list.")
                return None

        user_ids = df["user_id"].unique()

        cluster_list = []
        for id_ in user_ids:
            df_u = df.loc[df["user_id"] == id_]
            cluster_label = _get_cluster_label_for_user(df_u, cluster_cards)
            if cluster_label is not None:
                if print_results:
                    logger.info(f"User {id_} labeled card(s): {cluster_label}")
                if return_df_results:
                    cards = _get_cards_for_label(cluster_label, df_u)
                    cluster_list.append(
                        {"user_id": id_, "cluster_label": cluster_label, "cards": cards}
                    )
            else:
                if print_results:
                    logger.info(f"User {id_} did not cluster cards together.")

        if return_df_results:
            cluster_df = pd.DataFrame(cluster_list)
            return cluster_df
