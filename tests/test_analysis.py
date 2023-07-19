from cardsort import analysis
import pandas as pd
import pytest

df = pd.read_csv("tests/test-data.csv")
data_wrong_format = [
    [1, "Dog", 1, "canines", 1],
    [2, "Apple", 2, "food", 1],
    [3, "Cat", 3, "felines", 1],
    [3, "Cat", 4, "pets", 2],
    [1, "Dog", 4, "pets", 2],
    [2, "Apple", 5, "snacks", 2],
    [2, "Apple", 6, "fruit", 3],
    [3, "Cat", 7, "mammals", 3],
    [1, "Dog", 7, "mammals", 3],
    [1, "Dog", 7, "mammals", 3],  # duplicate row
]
columns = ["card_id", "card_label", "category_id", "category_label", "user_id"]
df_wrong_format = pd.DataFrame(data_wrong_format, columns=columns)


def test_check_data():
    expected = False
    actual = analysis._check_data(df_wrong_format)
    assert actual == expected, "Wrong data input correctly recognized"


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
    actual = analysis.get_cluster_labels(df, input, return_df_results=False)
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
    actual = analysis.get_cluster_labels(
        df=df,
        cluster_cards=input,
    )
    assert actual.equals(expected), "Dataframe does not equal expected dataframe"


def test_create_dendrogram_ve_count():
    with pytest.raises(ValueError):
        analysis.create_dendrogram(df, count="I am no count type!")


def test_create_dendrogram_ve_linkage():
    with pytest.raises(ValueError):
        analysis.create_dendrogram(df, linkage="I am no linkage type!")
