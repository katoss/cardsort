from cardsort import analysis
import pandas as pd
import pytest

df = pd.read_csv("tests/test-data.csv")


def test_get_distance_matrix():
    expected = [
        2.0,
        1.0,
        5.0,
        5.0,
        5.0,
        4.0,
        5.0,
        5.0,
        5.0,
        1.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        4.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        2.0,
        1.0,
        4.0,
        3.0,
        3.0,
        5.0,
        3.0,
        2.0,
        1.0,
        1.0,
        5.0,
        3.0,
        3.0,
        3.0,
        5.0,
        2.0,
        2.0,
        5.0,
        0.0,
        4.0,
        4.0,
    ]
    actual = analysis.get_distance_matrix(df)
    assert (actual == expected).all(), "Distance matrix not correct"


def test_get_cluster_labels():
    input = ["Cat", "Tiger", "Dog"]
    expected = ["pets", "animals", "Animals"]
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
    actual = analysis.get_cluster_labels_df(df, input)
    assert actual.equals(expected), "Dataframe does not equal expected dataframe"


def test_create_dendrogram_ve_count():
    with pytest.raises(ValueError):
        analysis.create_dendrogram(df, count="I am no count type!")


def test_create_dendrogram_ve_linkage():
    with pytest.raises(ValueError):
        analysis.create_dendrogram(df, linkage="I am no linkage type!")
