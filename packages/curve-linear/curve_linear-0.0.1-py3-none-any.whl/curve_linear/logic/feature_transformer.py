import numpy
from sklearn.base import (
    BaseEstimator,
    TransformerMixin
)
from sklearn import (
    pipeline,
    preprocessing,
    impute
)
import lightgbm


class FeatureTransformer(TransformerMixin, BaseEstimator):
    def __init__(self, is_cl, min_child_samples=100):
        self.is_cl = is_cl
        self.min_child_samples = min_child_samples
        self.imputer = impute.SimpleImputer()
        self.score_func = lambda model, x: (model.predict_proba(x)[:, 1] if is_cl else model.predict(x))
        self.std = preprocessing.StandardScaler()

    def fit(self, X, y):
        newX = self.imputer.fit_transform(X)
        self.feature_models = {
            i: self._train_monotonic_tree(newX[:, [i]], y)
            for i in range(newX.shape[1])
        }
        newX = self._transform_nonlinear(newX)
        self.std.fit(newX)
        return self

    def transform(self, X):
        return self.std.transform(self._transform_nonlinear(self.imputer.transform(X)))

    def _transform_nonlinear(self, X):
        return numpy.concatenate(
            [
                self._transform_each_features(X, i).reshape((X.shape[0], 1))
                for i in self.feature_models.keys()
            ], axis=1
        )

    def _transform_each_features(self, X, i):
        return sum(
            [
                self.score_func(model, X[:, [i]])
                for model in self.feature_models[i]
            ]
        )

    def _train_monotonic_tree(self, x, y):
        increasing_model = _get_model(self.is_cl, True, self.min_child_samples)
        decreasing_model = _get_model(self.is_cl, False, self.min_child_samples)
        increasing_model.fit(x, y)
        decreasing_model.fit(x, y)
        models = [increasing_model, decreasing_model]
        return self._select_models(x, y, models)

    def _select_models(self, x, y, models):
        features = numpy.concatenate(
            [
                self.score_func(models[i], x).reshape(x.shape[0], 1)
                for i in range(len(models))
            ], axis=1
        )
        selected_features = _select_features(x, y, features)
        return [models[i] if i >= 0 else AsIsFeature() for i in selected_features]


def _get_model(is_cl, is_increasing, min_child_samples):
    model = lightgbm.LGBMClassifier if is_cl else lightgbm.LGBMRegressor
    monotone_c = 1 if is_increasing else -1
    return model(monotone_constraints=monotone_c, min_child_samples=min_child_samples)


def _select_features(x, y, features):
    base_abs_corr = abs(_calc_corr(x[:, 0], y))
    abs_corr = [abs(_calc_corr(features[:, i], y)) for i in range(features.shape[1])]
    if all([abs_corr[i] <= base_abs_corr for i in range(features.shape[1])]):
        return [-1]
    else:
        return [i for i in range(features.shape[1]) if abs_corr[i] > base_abs_corr]


def _calc_corr(vec1, vec2):
    if numpy.std(vec1) == 0 or numpy.std(vec2) == 0:
        return 0
    else:
        return numpy.corrcoef(vec1, vec2)[0, 1]


class AsIsFeature(object):
    def predict(self, x):
        return x[:, 0]

    def predict_proba(self, x):
        return x[:, 0]
