from collections import Counter
from enum import Enum, auto
from typing import Any, Iterable, Iterator, Optional

import pandas as pd


class Type(Enum):
    TRUE_POSITIVE = auto()
    FALSE_POSITIVE = auto()
    FALSE_NEGATIVE = auto()
    TRUE_NEGATIVE = auto()
    NON_BINARY_SAME = auto()
    NON_BINARY_DIFF = auto()


TP = Type.TRUE_POSITIVE
FP = Type.FALSE_POSITIVE
FN = Type.FALSE_NEGATIVE
TN = Type.TRUE_NEGATIVE
NS = Type.NON_BINARY_SAME
ND = Type.NON_BINARY_DIFF


class TruthPair:

    predicted: Any
    actual: Any

    def __init__(self, predicted: Any, actual: Any) -> None:
        self.predicted = predicted
        self.actual = actual

    @property
    def type_(self) -> Type:
        if self.predicted == self.actual:
            return NS
        else:
            return ND


class BoolTruthPair(TruthPair):

    predicted: bool
    actual: bool

    def __init__(self, predicted: bool, actual: bool) -> None:
        if not isinstance(predicted, bool):
            predicted = bool(predicted)
        if not isinstance(actual, bool):
            actual = bool(actual)
        super().__init__(predicted, actual)

    @property
    def type_(self) -> Type:
        if self.predicted:
            return TP if self.actual else FP
        else:
            return FN if self.actual else TN


class ConfusionMatix:

    __is_binary: bool = True

    def __init__(
        self,
        iterable: Optional[Iterable[Type]] = None,
        *,
        count_tp: int = 0,
        count_fp: int = 0,
        count_fn: int = 0,
        count_tn: int = 0
    ) -> None:
        self.__count: Counter = Counter({
            TP: count_tp,
            FP: count_fp,
            FN: count_fn,
            TN: count_tn
        })
        if iterable is not None:
            if isinstance(iterable, Iterator):
                iterable = list(iterable)   # !!!
            self.__sanity_check(iterable)
            self.__count.update(iterable)

    def __sanity_check(self, iterable: Iterable[Type]) -> None:
        for i in iterable:
            if not isinstance(i, Type):
                raise TypeError(
                    'value in argument `iterable` must be '
                    'instance of `Type`'
                )
            if i in (NS, ND) and self.__is_binary:
                self.__is_binary = False

    def clear(self) -> None:
        self.__count.clear()

    reset = clear

    def update(
        self,
        iterable: Optional[Iterable[Type]] = None,
        *,
        count_tp: int = 0,
        count_fp: int = 0,
        count_fn: int = 0,
        count_tn: int = 0
    ) -> None:
        self.__count[TP] += count_tp
        self.__count[FP] += count_fp
        self.__count[FN] += count_fn
        self.__count[TN] += count_tn
        if iterable is not None:
            if isinstance(iterable, Iterator):
                iterable = list(iterable)
            self.__sanity_check(iterable)
            self.__count.update(iterable)

    @property
    def matrix(self) -> pd.DataFrame:
        assert self.__is_binary
        matrix = pd.DataFrame(
            index=['Predicted Positive', 'Predicted Negative'],
            columns=['Actual Positive', 'Actual Negative']
        )
        matrix.iloc[0, 0] = self.__count[TP]
        matrix.iloc[0, 1] = self.__count[FP]
        matrix.iloc[1, 0] = self.__count[FN]
        matrix.iloc[1, 1] = self.__count[TN]
        return matrix

    @property
    def accuracy(self) -> float:
        """
        accuracy = (TP + TN) / (TP + TN + FP + FN)

        Return NaN for `ZeroDivisionError`.

        This property assumes that attribute `__count` only contains keys
        specified in method `__init__`.
        """
        try:
            if self.__is_binary:
                return (
                    self.__count[TP] + self.__count[TN]
                ) / self.__count.total()
            else:
                return (
                    self.__count[TP] + self.__count[TN] + self.__count[NS]
                ) / self.__count.total()
        except ZeroDivisionError:
            return float('nan')

    ACC = accuracy

    @property
    def sensitivity(self) -> float:
        """
        sensitivity = TP / (TP + FN)

        Return NaN for `ZeroDivisionError`.
        """
        assert self.__is_binary
        try:
            return self.__count[TP] / (self.__count[TP] + self.__count[FN])
        except ZeroDivisionError:
            return float('nan')

    recall = hit_rate = true_positive_rate = TPR = sensitivity

    @property
    def specificity(self) -> float:
        """
        specificity = TN / (TN + FP)

        Return NaN for `ZeroDivisionError`.
        """
        assert self.__is_binary
        try:
            return self.__count[TN] / (self.__count[TN] + self.__count[FP])
        except ZeroDivisionError:
            return float('nan')

    selectivity = true_negative_rate = TNR = specificity

    @property
    def F1_score(self) -> float:
        """
        F1_score = 2TP / (2TP + FP + FN)

        Return NaN for `ZeroDivisionError`.
        """
        assert self.__is_binary
        try:
            return self.__count[TP] * 2 / (
                self.__count[TP] * 2 +
                self.__count[FP] +
                self.__count[FN]
            )
        except ZeroDivisionError:
            return float('nan')

    @property
    def statistics(self) -> pd.DataFrame:
        if self.__is_binary:
            stats = pd.DataFrame({
                'accuracy': {
                    'alias': 'ACC',
                    'formula': '(TP + TN) / (TP + TN + FP + FN)',
                    'value': self.accuracy
                },
                'sensitivity': {
                    'alias': 'recall, hit rate, true positive rate, TPR',
                    'formula': 'TP / (TP + FN)',
                    'value': self.sensitivity
                },
                'specificity': {
                    'alias': 'selectivity, true negative rate, TNR',
                    'formula': 'TN / (TN + FP)',
                    'value': self.specificity
                },
                'F1_score': {
                    'alias': 'N/A',
                    'formula': '2TP / (2TP + FP + FN)',
                    'value': self.F1_score
                },
            }).T
        else:
            stats = pd.DataFrame({
                'accuracy': {
                    'alias': 'ACC',
                    'formula': 'T / T + F',
                    'value': self.accuracy
                }
            }).T
        stats['value'] = stats['value'].apply(pd.to_numeric)
        return stats

    stats = statistics

    def _repr_html_(self) -> str:
        try:
            matrix_html = self.matrix._repr_html_()
        except AssertionError:
            matrix_html = 'Not Available.'
        stats_html = self.statistics._repr_html_()
        return f"""
            <div>
                <h4>Confusion Matrix</h4>
                    <div>{matrix_html}</div>
                <h4>Statistics</h4>
                    <div>{stats_html}</div>
            </div>
        """
