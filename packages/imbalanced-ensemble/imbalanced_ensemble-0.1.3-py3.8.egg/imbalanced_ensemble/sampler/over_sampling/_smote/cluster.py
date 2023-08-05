"""SMOTE variant employing some clustering before the generation."""
# Adapted from imbalanced-learn

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Fernando Nogueira
#          Christos Aridas
#          Zhining Liu <zhining.liu@outlook.com>
# License: MIT

import math

import numpy as np
from scipy import sparse

from sklearn.base import clone
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import pairwise_distances
from sklearn.utils import _safe_indexing
from sklearn.preprocessing import normalize


from .base import BaseSMOTE
from ..base import BaseOverSampler
from ....utils._docstring import _n_jobs_docstring, Substitution
from ....utils._docstring import _random_state_docstring
from ....utils._validation import _deprecate_positional_args

# # For local test
# import sys
# sys.path.append("../../..")
# from sampler.over_sampling._smote.base import BaseSMOTE
# from sampler.over_sampling.base import BaseOverSampler
# from utils._docstring import _n_jobs_docstring, Substitution
# from utils._docstring import _random_state_docstring
# from utils._validation import _deprecate_positional_args


@Substitution(
    sampling_strategy=BaseOverSampler._sampling_strategy_docstring,
    n_jobs=_n_jobs_docstring,
    random_state=_random_state_docstring,
)
class KMeansSMOTE(BaseSMOTE):
    """Apply a KMeans clustering before to over-sample using SMOTE.

    This is an implementation of the algorithm described in [1]_.

    Read more in the `User Guide <https://imbalanced-learn.org/stable/over_sampling.html#smote-adasyn>`_.

    Parameters
    ----------
    {sampling_strategy}

    {random_state}

    k_neighbors : int or object, default=2
        If ``int``, number of nearest neighbours to used to construct synthetic
        samples.  If object, an estimator that inherits from
        :class:`~sklearn.neighbors.base.KNeighborsMixin` that will be used to
        find the k_neighbors.

    {n_jobs}

    kmeans_estimator : int or object, default=None
        A KMeans instance or the number of clusters to be used. By default,
        we used a :class:`~sklearn.cluster.MiniBatchKMeans` which tend to be
        better with large number of samples.

    cluster_balance_threshold : "auto" or float, default="auto"
        The threshold at which a cluster is called balanced and where samples
        of the class selected for SMOTE will be oversampled. If "auto", this
        will be determined by the ratio for each class, or it can be set
        manually.

    density_exponent : "auto" or float, default="auto"
        This exponent is used to determine the density of a cluster. Leaving
        this to "auto" will use a feature-length based exponent.

    Attributes
    ----------
    kmeans_estimator_ : estimator
        The fitted clustering method used before to apply SMOTE.

    nn_k_ : estimator
        The fitted k-NN estimator used in SMOTE.

    cluster_balance_threshold_ : float
        The threshold used during ``fit`` for calling a cluster balanced.

    See Also
    --------
    SMOTE : Over-sample using SMOTE.
    
    SVMSMOTE : Over-sample using SVM-SMOTE variant.

    BorderlineSMOTE : Over-sample using Borderline-SMOTE variant.

    ADASYN : Over-sample using ADASYN.

    Notes
    -----
    See the original papers: [1]_ for more details.

    Supports multi-class resampling. A one-vs.-rest scheme is used.

    References
    ----------
    .. [1] Felix Last, Georgios Douzas, Fernando Bacao, "Oversampling for
       Imbalanced Learning Based on K-Means and SMOTE"
       https://arxiv.org/abs/1711.00837

    Examples
    --------
    >>> import numpy as np
    >>> from imbalanced_ensemble.sampler.over_sampling import KMeansSMOTE
    >>> from sklearn.datasets import make_blobs
    >>> blobs = [100, 800, 100]
    >>> X, y  = make_blobs(blobs, centers=[(-10, 0), (0,0), (10, 0)])
    >>> # Add a single 0 sample in the middle blob
    >>> X = np.concatenate([X, [[0, 0]]])
    >>> y = np.append(y, 0)
    >>> # Make this a binary classification problem
    >>> y = y == 1
    >>> sm = KMeansSMOTE(random_state=42)
    >>> X_res, y_res = sm.fit_resample(X, y)
    >>> # Find the number of new samples in the middle blob
    >>> n_res_in_middle = ((X_res[:, 0] > -5) & (X_res[:, 0] < 5)).sum()
    >>> print("Samples in the middle blob: %s" % n_res_in_middle)
    Samples in the middle blob: 801
    >>> print("Middle blob unchanged: %s" % (n_res_in_middle == blobs[1] + 1))
    Middle blob unchanged: True
    >>> print("More 0 samples: %s" % ((y_res == 0).sum() > (y == 0).sum()))
    More 0 samples: True
    """

    @_deprecate_positional_args
    def __init__(
        self,
        *,
        sampling_strategy="auto",
        random_state=None,
        k_neighbors=2,
        n_jobs=None,
        kmeans_estimator=None,
        cluster_balance_threshold="auto",
        density_exponent="auto",
    ):
        super().__init__(
            sampling_strategy=sampling_strategy,
            random_state=random_state,
            k_neighbors=k_neighbors,
            n_jobs=n_jobs,
        )
        self.kmeans_estimator = kmeans_estimator
        self.cluster_balance_threshold = cluster_balance_threshold
        self.density_exponent = density_exponent

    def _validate_estimator(self):
        super()._validate_estimator()
        if self.kmeans_estimator is None:
            self.kmeans_estimator_ = MiniBatchKMeans(
                batch_size=4096, 
                random_state=self.random_state,
            )
        elif isinstance(self.kmeans_estimator, int):
            self.kmeans_estimator_ = MiniBatchKMeans(
                batch_size=4096, 
                n_clusters=self.kmeans_estimator,
                random_state=self.random_state,
            )
        else:
            self.kmeans_estimator_ = clone(self.kmeans_estimator)

        # validate the parameters
        for param_name in ("cluster_balance_threshold", "density_exponent"):
            param = getattr(self, param_name)
            if isinstance(param, str) and param != "auto":
                raise ValueError(
                    f"'{param_name}' should be 'auto' when a string is passed."
                    f" Got {repr(param)} instead."
                )

        self.cluster_balance_threshold_ = (
            self.cluster_balance_threshold
            if self.kmeans_estimator_.n_clusters != 1
            else -np.inf
        )

    def _find_cluster_sparsity(self, X):
        """Compute the cluster sparsity."""
        euclidean_distances = pairwise_distances(
            X, metric="euclidean", n_jobs=self.n_jobs
        )
        # negate diagonal elements
        for ind in range(X.shape[0]):
            euclidean_distances[ind, ind] = 0

        non_diag_elements = (X.shape[0] ** 2) - X.shape[0]
        mean_distance = euclidean_distances.sum() / non_diag_elements
        exponent = (
            math.log(X.shape[0], 1.6) ** 1.8 * 0.16
            if self.density_exponent == "auto"
            else self.density_exponent
        )
        return (mean_distance ** exponent) / X.shape[0]

    def _fit_resample(self, X, y, sample_weight=None):
        self._validate_estimator()
        X_resampled = X.copy()
        y_resampled = y.copy()
        total_inp_samples = sum(self.sampling_strategy_.values())

        for class_sample, n_samples in self.sampling_strategy_.items():
            if n_samples == 0:
                continue

            # target_class_indices = np.flatnonzero(y == class_sample)
            # X_class = _safe_indexing(X, target_class_indices)

            X_clusters = self.kmeans_estimator_.fit_predict(X)
            valid_clusters = []
            cluster_sparsities = []

            # identify cluster which are answering the requirements
            for cluster_idx in range(self.kmeans_estimator_.n_clusters):

                cluster_mask = np.flatnonzero(X_clusters == cluster_idx)
                X_cluster = _safe_indexing(X, cluster_mask)
                y_cluster = _safe_indexing(y, cluster_mask)

                cluster_class_mean = (y_cluster == class_sample).mean()

                if self.cluster_balance_threshold_ == "auto":
                    balance_threshold = n_samples / total_inp_samples / 2
                else:
                    balance_threshold = self.cluster_balance_threshold_

                # the cluster is already considered balanced
                if cluster_class_mean < balance_threshold:
                    continue

                # not enough samples to apply SMOTE
                anticipated_samples = cluster_class_mean * X_cluster.shape[0]
                if anticipated_samples < self.nn_k_.n_neighbors:
                    continue

                X_cluster_class = _safe_indexing(
                    X_cluster, np.flatnonzero(y_cluster == class_sample)
                )

                valid_clusters.append(cluster_mask)
                cluster_sparsities.append(self._find_cluster_sparsity(X_cluster_class))

            cluster_sparsities = np.array(cluster_sparsities)
            cluster_weights = cluster_sparsities / cluster_sparsities.sum()
            cluster_n_samples_list = np.zeros_like(cluster_weights)
            
            # if class_sample == 1:
            #     print (n_samples)
            #     print (cluster_weights)
            #     print ([math.ceil(
            #         n_samples * cluster_weights[valid_cluster_idx] - 1e-3
            #         ) for valid_cluster_idx, _ in enumerate(valid_clusters)])
            #     print (cluster_n_samples)

            if not valid_clusters:
                raise RuntimeError(
                    f"No clusters found with sufficient samples of "
                    f"class {class_sample}. Try lowering the "
                    f"cluster_balance_threshold or increasing the number of "
                    f"clusters."
                )

            for valid_cluster_idx, valid_cluster in enumerate(valid_clusters):
                X_cluster = _safe_indexing(X, valid_cluster)
                y_cluster = _safe_indexing(y, valid_cluster)

                X_cluster_class = _safe_indexing(
                    X_cluster, np.flatnonzero(y_cluster == class_sample)
                )

                self.nn_k_.fit(X_cluster_class)
                nns = self.nn_k_.kneighbors(X_cluster_class, return_distance=False)[
                    :, 1:
                ]

                if valid_cluster_idx == self.kmeans_estimator_.n_clusters - 1:
                    cluster_n_samples = int(n_samples - sum(cluster_n_samples_list))
                else:
                    cluster_n_samples = math.floor(
                        n_samples * cluster_weights[valid_cluster_idx]
                    )
                cluster_n_samples_list[valid_cluster_idx] = cluster_n_samples

                X_new, y_new = self._make_samples(
                    X_cluster_class,
                    y.dtype,
                    class_sample,
                    X_cluster_class,
                    nns,
                    cluster_n_samples,
                    1.0,
                )

                stack = [np.vstack, sparse.vstack][int(sparse.issparse(X_new))]
                X_resampled = stack((X_resampled, X_new))
                y_resampled = np.hstack((y_resampled, y_new))
        
        # If given sample_weight
        if sample_weight is not None:
            # sample_weight is already validated in self.fit_resample()
            sample_weight_new = \
                np.empty(y_resampled.shape[0] - y.shape[0], dtype=np.float64)
            sample_weight_new[:] = np.mean(sample_weight)
            sample_weight_resampled = np.hstack([sample_weight, sample_weight_new]).reshape(-1, 1)
            sample_weight_resampled = \
                np.squeeze(normalize(sample_weight_resampled, axis=0, norm='l1'))
            return X_resampled, y_resampled, sample_weight_resampled
        else: return X_resampled, y_resampled
