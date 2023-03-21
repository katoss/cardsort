from cardsort import analysis
import pandas as pd

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