__all__ = [
    "get_distance_matrix",
    "create_dendrogram",
    "get_cluster_labels",
    "get_cluster_labels_df",
]

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform


def _get_distance_matrix_for_user(df_user):
    n = len(df_user)

    X = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            cat1 = df_user.query("card_id==" + str(i + 1))["category_label"].values[0]
            cat2 = df_user.query("card_id==" + str(j + 1))["category_label"].values[0]
            if cat1 == cat2:
                X[i, j] = 0
            else:
                X[i, j] = 1
            j += i
        i += 1
    return X


def get_distance_matrix(df):
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
    id = 1
    while id <= max(df.user_id):
        df_u = df.loc[df["user_id"] == id]
        print("Computing distance matrix for user " + str(id))
        distance_matrix_user = _get_distance_matrix_for_user(df_u)
        if id == 1:
            distance_matrix_all = distance_matrix_user
        else:
            distance_matrix_all = np.add(distance_matrix_all, distance_matrix_user)
        id += 1
    condensed_distance_matrix = squareform(distance_matrix_all)
    return condensed_distance_matrix


def create_dendrogram(
    df, distance_matrix=None, count="fraction", linkage="average", color_treshold=None
):
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

    color_treshold : double, optional
        Level below which to cut the color threshold in the dendrogram branches.
        Can be a fraction (0 - 1) or an absolute value (<= n = number of users).
        The default cut is at 75%.
    """

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
        if color_treshold == None:
            color_treshold = 0.75
    else:
        if color_treshold == None:
            color_treshold = np.max(distance_matrix) * 0.75

    Z = hierarchy.linkage(distance_matrix, linkage)
    plt.figure(layout="constrained")
    labels = df.loc[df["user_id"] == 1]["card_label"].squeeze().to_list()
    dn = hierarchy.dendrogram(
        Z, labels=labels, orientation="right", color_threshold=color_treshold
    )

    x_max = np.max(distance_matrix)
    if x_max <= 1:
        plt.xticks(np.arange(0.0, 1.1, 0.1))
    else:
        plt.xticks(np.arange(0, x_max + 1, 1))
    for leaf, leaf_color in zip(plt.gca().get_yticklabels(), dn["leaves_color_list"]):
        leaf.set_color(leaf_color)
    plt.show()


def _get_cluster_label_for_user(df_u, cluster_cards):
    cat_before = ""
    for index, card in enumerate(cluster_cards):
        try:
            cat = df_u.query('card_label=="' + card + '"')["category_label"].values[0]
            if cat_before != "":
                if cat == cat_before:
                    continue
                else:
                    return
            cat_before = cat
            index += 1
        except IndexError:
            print('"' + card + '" is not a valid card label. Removed from list.')
            cluster_cards.remove(card)
            print("Continue with cards: %s" % cluster_cards)
    return cat


def _get_cards_for_label(cluster_label, df_u):
    cards_list = df_u.query('category_label=="' + cluster_label + '"')[
        "card_label"
    ].tolist()
    return cards_list


def get_cluster_labels(df, cluster_cards):
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

    Returns
    -------
    out : list of str
        Contains cluster-labels from all users who grouped the given cards together. 
    """

    cluster_labels = []
    id = 1
    while id <= max(df.user_id):
        df_u = df.loc[df["user_id"] == id]
        try:
            cluster_label = _get_cluster_label_for_user(df_u, cluster_cards)
            if cluster_label is not None:
                print("User " + str(id) + " labeled card(s): " + cluster_label)
                cluster_labels.append(cluster_label)
            else:
                print("User " + str(id) + " did not cluster cards together.")
        except UnboundLocalError:
            print("No cards left in list.")
            break
        id += 1
    return cluster_labels


def get_cluster_labels_df(df, cluster_cards):
    """
    Return category labels and user id for each user who clustered given list of cards together.
    Also returns full list of cards in that category.

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

    Returns
    -------
    out : pandas.DataFrame
        Columns:
            Name: user_id, int
            Name: cluster_label, str
            Name: cards, list of str
        Dataframe with one row for each user who clustered the given cards together, including category label and 
        the full list of cards in that category. 
    """

    cluster_df = pd.DataFrame(columns=["user_id", "cluster_label", "cards"])
    id = 1
    while id <= max(df.user_id):
        df_u = df.loc[df["user_id"] == id]
        try:
            cluster_label = _get_cluster_label_for_user(df_u, cluster_cards)
            if cluster_label is not None:
                print("User " + str(id) + " labeled card(s): " + cluster_label)
                cards = _get_cards_for_label(cluster_label, df_u)
                cluster_df = pd.concat(
                    [
                        cluster_df,
                        pd.DataFrame.from_records(
                            [
                                {
                                    "user_id": id,
                                    "cluster_label": cluster_label,
                                    "cards": cards,
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                )
            else:
                print("User " + str(id) + " did not cluster cards together.")
        except UnboundLocalError:
            print("No cards left in list.")
            break
        id += 1
    return cluster_df
