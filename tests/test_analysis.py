from cardsort import analysis
import pandas as pd
import pytest

df = pd.read_csv("tests/test-data.csv")


def test_get_distance_matrix():
    # fmt: off
    expected = [2., 1., 5., 5., 5., 4., 5., 5., 5., 1., 5., 5., 
                5., 5., 5., 5., 4., 5., 5., 5., 5., 5., 5., 5.,
                2., 1., 4., 3., 3., 5., 3., 2., 1., 1., 5., 3., 
                3., 3., 5., 2., 2., 5., 0., 4., 4.]
    # fmt: on
    actual = analysis.get_distance_matrix(df)
    assert (actual == expected).all(), "Distance matrix not correct"


def test_get_cluster_labels_print():
    input = ["Cat", "Tiger", "Dog"]
    expected = None
    actual = analysis.get_cluster_labels(df, input)
    assert actual == expected, "Test data cluster labels incorrectly retreived"


def test_get_cluster_labels_df():
    input = ["Cat", "Tiger", "Dog"]
    data_exp = [
        [1, "pets", ["Dog", "Tiger", "Cat"]],
        [2, "animals", ["Cat", "Tiger", "Dog"]],
        [5, "Animals", ["Dog", "Tiger", "Cat"]],
    ]
    expected = pd.DataFrame(data_exp, columns=["user_id", "cluster_label", "cards"])
    expected = expected.astype({"user_id": "object"})
    actual = analysis.get_cluster_labels(df, input, return_df_results=True)
    assert actual.equals(expected), "Dataframe does not equal expected dataframe"


def test_create_dendrogram_ve_count():
    with pytest.raises(ValueError):
        analysis.create_dendrogram(df, count="I am no count type!")


def test_create_dendrogram_ve_linkage():
    with pytest.raises(ValueError):
        analysis.create_dendrogram(df, linkage="I am no linkage type!")
