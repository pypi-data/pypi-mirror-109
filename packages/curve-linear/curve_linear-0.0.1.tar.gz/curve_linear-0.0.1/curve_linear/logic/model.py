from sklearn import linear_model
from sklearn.base import BaseEstimator

from curve_linear.logic import feature_transformer


class CurveLinearModel(BaseEstimator):
    def __init__(self, min_child_samples=100, penalty="l1", C=1):
        super(CurveLinearModel, self).__init__()
        self.min_child_samples = min_child_samples
        self.penalty = penalty
        self.C = C

    def fit(self, X, y):
        self.feature_transformer_ = self._get_feature_transformer()
        self.linear_model_ = self._get_linear_model()
        self.feature_transformer_.fit(X, y)
        self.linear_model_.fit(self.feature_transformer_.transform(X), y)
        self.coef_ = self.linear_model_.coef_
        self.intercept_ = self.linear_model_.intercept_
        return self

    def predict(self, X):
        return self.linear_model_.predict(
            self.feature_transformer_.transform(X)
        )

    def predict_proba(self, X):
        return self.linear_model_.predict_proba(
            self.feature_transformer_.transform(X)
        )


class CurveLinearClassifier(CurveLinearModel):
    def _get_linear_model(self):
        return linear_model.LogisticRegression(penalty=self.penalty, C=self.C, solver="liblinear")

    def _get_feature_transformer(self):
        return feature_transformer.FeatureTransformer(is_cl=True, min_child_samples=self.min_child_samples)


class CurveLinearRegressor(CurveLinearModel):
    def _get_linear_model(self):
        if self.penalty=="l1":
            return linear_model.Lasso(alpha=1./self.C)
        elif self.penalty=="l2":
            return linear_model.Ridge(alpha=1./self.C)
        else:
            raise Exception("penalty={} is not supported".format(self.penalty))

    def _get_feature_transformer(self):
        return feature_transformer.FeatureTransformer(is_cl=False, min_child_samples=self.min_child_samples)
