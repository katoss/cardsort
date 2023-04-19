from cardsort import analysis
import pandas as pd
import pytest

def test_get_distance_matrix():
    df = pd.read_csv('tests/test-data.csv')
    expected = [2., 1., 5., 5., 5., 4., 5., 5., 5., 1., 5., 5., 
                5., 5., 5., 5., 4., 5., 5., 5., 5., 5., 5., 5.,
                2., 1., 4., 3., 3., 5., 3., 2., 1., 1., 5., 3., 
                3., 3., 5., 2., 2., 5., 0., 4., 4.]
    actual = analysis.get_distance_matrix(df)
    assert (actual == expected).all(), "Distance matrix not correct"

def test_get_cluster_labels():
    input = ['Cat', 'Tiger', 'Dog']
    df = pd.read_csv('tests/test-data.csv')
    expected = ['pets', 'animals', 'Animals']
    actual = analysis.get_cluster_labels(df, input)
    assert actual == expected, "Test data cluster labels incorrectly retreived"

def test_get_cluster_labels_df():
    input = ['Cat', 'Tiger', 'Dog']
    df = pd.read_csv('tests/test-data.csv')
    data_exp = [[1, "pets", ["Dog", "Tiger", "Cat"]],[2, "animals", ["Cat", "Tiger", "Dog"]],[5, "Animals", ["Dog", "Tiger", "Cat"]]] 
    expected = pd.DataFrame(data_exp, columns=["user_id", "cluster_label", "cards"])
    expected = expected.astype({'user_id' : 'object'})
    actual = analysis.get_cluster_labels_df(df,input)
    assert actual.equals(expected), "Dataframe does not equal expected dataframe"