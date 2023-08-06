from typing import List

import numpy as np
import pandas as pd

from model_quality_report.model_base import ModelBase
from model_quality_report.quality_metrics import RegressionQualityMetrics
from model_quality_report.quality_report.base import (
    QualityReportBase,
)
from model_quality_report.splitters.base import SplitterBase


class CrossValidationTimeSeriesQualityReport(QualityReportBase):
    """Cross-validation time series quality report.

    Collects quality metrics when model predictions are in general non-scalar, e.g. for several time steps ahead.

    """

    lbl_horizon = "horizon"

    def __init__(self, model: ModelBase, splitter: SplitterBase) -> None:
        super().__init__(model=model, splitter=splitter)

    @staticmethod
    def _calculate_quality_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict:
        metric_dict = dict()
        for metric_name in [
            RegressionQualityMetrics.lbl_explained_variance_score,
            RegressionQualityMetrics.lbl_mean_absolute_percentage_error,
            RegressionQualityMetrics.lbl_median_absolute_percentage_error,
            RegressionQualityMetrics.lbl_mean_absolute_error,
            RegressionQualityMetrics.lbl_mean_squared_error,
            RegressionQualityMetrics.lbl_median_absolute_error,
            RegressionQualityMetrics.lbl_r2_score,
        ]:
            metric_dict[metric_name] = getattr(RegressionQualityMetrics, metric_name)(y_true, y_pred)

        return metric_dict

    def _calculate_quality_metrics_as_pandas(self, y_true: pd.DataFrame, y_pred: pd.DataFrame) -> pd.DataFrame:
        return (
            y_true.join(y_pred)
            .dropna()
            .groupby(self.lbl_horizon)
            .apply(
                lambda df_true_pred: pd.Series(
                    self._calculate_quality_metrics(
                        df_true_pred[self.lbl_true_values],
                        df_true_pred[self.lbl_predicted_values],
                    )
                )
            )
            .rename_axis(self.lbl_metrics, axis=1)
            .rename_axis(self.lbl_horizon, axis=0)
            .stack()
            .rename(self.lbl_metric_value)
            .reset_index()
        )

    def _convert_list_of_data_to_pandas(self, data: List[pd.Series], name: str = None) -> pd.DataFrame:
        df_list = [pd.DataFrame({name: s, self.lbl_horizon: np.arange(s.shape[0])}) for s in data]
        return pd.concat(df_list).set_index(self.lbl_horizon, append=True)
