"""Test the module cluster centroids."""
from collections import Counter

import pytest
import numpy as np
from scipy import sparse

from sklearn.cluster import KMeans
from sklearn.datasets import make_classification

from imbalanced_ensemble.sampler.under_sampling import ClusterCentroids

RND_SEED = 0
X = np.array(
    [
        [0.04352327, -0.20515826],
        [0.92923648, 0.76103773],
        [0.20792588, 1.49407907],
        [0.47104475, 0.44386323],
        [0.22950086, 0.33367433],
        [0.15490546, 0.3130677],
        [0.09125309, -0.85409574],
        [0.12372842, 0.6536186],
        [0.13347175, 0.12167502],
        [0.094035, -2.55298982],
    ]
)
Y = np.array([1, 0, 1, 0, 1, 1, 1, 1, 0, 1])
R_TOL = 1e-4


@pytest.mark.parametrize(
    "X, expected_voting", [(X, "soft"), (sparse.csr_matrix(X), "hard")]
)
def test_fit_resample_check_voting(X, expected_voting):
    cc = ClusterCentroids(random_state=RND_SEED)
    cc.fit_resample(X, Y)
    assert cc.voting_ == expected_voting


def test_fit_resample_auto():
    sampling_strategy = "auto"
    cc = ClusterCentroids(sampling_strategy=sampling_strategy, random_state=RND_SEED)
    X_resampled, y_resampled = cc.fit_resample(X, Y)
    assert X_resampled.shape == (6, 2)
    assert y_resampled.shape == (6,)


def test_fit_resample_half():
    sampling_strategy = {0: 3, 1: 6}
    cc = ClusterCentroids(sampling_strategy=sampling_strategy, random_state=RND_SEED)
    X_resampled, y_resampled = cc.fit_resample(X, Y)
    assert X_resampled.shape == (9, 2)
    assert y_resampled.shape == (9,)


def test_multiclass_fit_resample():
    y = Y.copy()
    y[5] = 2
    y[6] = 2
    cc = ClusterCentroids(random_state=RND_SEED)
    _, y_resampled = cc.fit_resample(X, y)
    count_y_res = Counter(y_resampled)
    assert count_y_res[0] == 2
    assert count_y_res[1] == 2
    assert count_y_res[2] == 2


def test_fit_resample_object():
    sampling_strategy = "auto"
    cluster = KMeans(random_state=RND_SEED)
    cc = ClusterCentroids(
        sampling_strategy=sampling_strategy, random_state=RND_SEED, estimator=cluster,
    )

    X_resampled, y_resampled = cc.fit_resample(X, Y)
    assert X_resampled.shape == (6, 2)
    assert y_resampled.shape == (6,)


def test_fit_hard_voting():
    sampling_strategy = "auto"
    voting = "hard"
    cluster = KMeans(random_state=RND_SEED)
    cc = ClusterCentroids(
        sampling_strategy=sampling_strategy,
        random_state=RND_SEED,
        estimator=cluster,
        voting=voting,
    )

    X_resampled, y_resampled = cc.fit_resample(X, Y)
    assert X_resampled.shape == (6, 2)
    assert y_resampled.shape == (6,)
    for x in X_resampled:
        assert np.any(np.all(x == X, axis=1))


@pytest.mark.parametrize(
    "cluster_centroids_params, err_msg",
    [
        ({"estimator": "rnd"}, "has to be a KMeans clustering"),
        ({"voting": "unknown"}, "needs to be one of"),
    ],
)
def test_fit_resample_error(cluster_centroids_params, err_msg):
    cc = ClusterCentroids(**cluster_centroids_params)
    with pytest.raises(ValueError, match=err_msg):
        cc.fit_resample(X, Y)


def test_cluster_centroids_n_jobs():
    # check that we deprecate the `n_jobs` parameter.
    cc = ClusterCentroids(n_jobs=1)
    with pytest.warns(FutureWarning) as record:
        cc.fit_resample(X, Y)
    assert len(record) == 1
    assert "'n_jobs' was deprecated" in record[0].message.args[0]


def test_cluster_centroids_hard_target_class():
    # check that the samples selecting by the hard voting corresponds to the
    # targeted class
    # non-regression test for:
    # https://github.com/scikit-learn-contrib/imbalanced-learn/issues/738
    X, y = make_classification(
        n_samples=1000,
        n_features=2,
        n_informative=1,
        n_redundant=0,
        n_repeated=0,
        n_clusters_per_class=1,
        weights=[0.3, 0.7],
        class_sep=0.01,
        random_state=0,
    )

    cc = ClusterCentroids(voting="hard", random_state=0)
    X_res, y_res = cc.fit_resample(X, y)

    minority_class_indices = np.flatnonzero(y == 0)
    X_minority_class = X[minority_class_indices]

    resampled_majority_class_indices = np.flatnonzero(y_res == 1)
    X_res_majority = X_res[resampled_majority_class_indices]

    sample_from_minority_in_majority = [
        np.all(np.isclose(selected_sample, minority_sample))
        for selected_sample in X_res_majority
        for minority_sample in X_minority_class
    ]
    assert sum(sample_from_minority_in_majority) == 0
