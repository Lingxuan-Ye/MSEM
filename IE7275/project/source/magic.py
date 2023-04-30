from pathlib import Path
from typing import (Any, Callable, Dict, Iterable, Literal, NamedTuple,
                    Optional, TypeVar, Union, overload)

import numpy as np
import pandas as pd
from IPython.display import HTML, display
from sklearn.decomposition import PCA
from sklearn.model_selection import KFold, train_test_split

try:
    from .constants import PARAMS
    from .evaluation import BoolTruthPair, ConfusionMatix, TruthPair
except ImportError:  # for debugging
    from constants import PARAMS  # type: ignore
    from evaluation import (BoolTruthPair, ConfusionMatix,  # type: ignore
                            TruthPair)

# `Self` is not supported until Python 3.11
# return `self` for method chaining
Self = TypeVar('Self', bound='Magic')
Estimator = Any


class FormatError(Exception):
    pass


class Args(NamedTuple):
    """
    Set default value to Mutable is never a good choice,
    for example, `kwargs = {}` should never be considered.
    """
    args: tuple = ()
    kwargs: Dict[str, Any] = dict()


class PCA_Result(NamedTuple):
    summary: pd.DataFrame
    components: pd.DataFrame
    scores: pd.DataFrame


class BestResult(NamedTuple):

    combinations: np.ndarray[tuple, np.dtype[np.object_]]
    scores: np.ndarray[float, np.dtype[np.float_]]

    def _repr_html_(self) -> str:
        tab = '&nbsp;' * 4
        item = '\n'.join(
            f"""
            <li>
            <p><b>Parameters</b></p>
            <p>{tab}Estimator type: {j[0].__name__}, Drop NaN: {j[1]}</p>
            <p>{tab}Convert categoricals: {j[2]}, Convert by: {j[3]}</p>
            <p>{tab}Normalize data: {j[4]}, Normalize by: {j[5]}</p>
            <p>{tab}PCA-Decomposite: {j[6]}</p>
            <p><b>Accuracy</b></p>
            <p>{tab}{self.scores[i]}</p>
            </li>
            """
            for i, j in enumerate(self.combinations)
        )
        return f"""
            <h2>Top-{len(self.combinations)} Conbinations</h2>
                <ol>
                    {item}
                </ol>
        """


class Magic:

    read_from: Optional[Path]
    y_label: str

    __raw: pd.DataFrame
    __y: pd.Series
    __positive: Optional[str]
    __data: pd.DataFrame
    __estimator: Optional[Estimator] = None
    __cache: Optional[pd.DataFrame] = None

    @overload
    def __init__(
        self,
        dataset: Path,
        y_label: str,
        positive: Optional[str],
        estimator: Optional[Estimator],
        *,
        read_args: Optional[Args],
        preprocess_args: Optional[Args]
    ) -> None:
        pass

    @overload
    def __init__(
        self,
        dataset: str,
        y_label: str,
        positive: Optional[str],
        estimator: Optional[Estimator],
        *,
        read_args: Optional[Args],
        preprocess_args: Optional[Args]
    ) -> None:
        pass

    @overload
    def __init__(
        self,
        dataset: pd.DataFrame,
        y_label: str,
        positive: Optional[str],
        estimator: Optional[Estimator],
        *,
        read_args: Optional[Args],
        preprocess_args: Optional[Args]
    ) -> None:
        pass

    def __init__(
        self,
        dataset,
        y_label,
        positive=None,
        estimator=None,
        *,
        read_args=None,
        preprocess_args=None
    ) -> None:
        """
        Parameters
        ----------
        dataset : Path | str | pd.DataFrame
            Dataset source.
        y_label : str
            Determine which column is classification objective.
        positive : Optional[str], optional
            Mark specified class as positive.
        estimator : Estimator
            Estimator instance.

        Raises
        ------
        TypeError
            _description_
        Please carefully read `self.read.__doc__`
        and `self.preprocess.__doc__`.

        Examples
        --------
        - A complete read_args should be like this:

            ```
            Args(
                args=(),
                kwargs={
                    'func': None,
                    'func_args': Args()
                }
            )
            ```

        - A complete preprocess_args should be like this:

            ```
            Args(
                args=(),
                kwargs={
                    'dropna': True,
                    'dropna_args': Args(),
                    'numerify': True,
                    'numerify_args': Args(
                        args=('codes',),
                        kwargs={'func': None, 'func_args': Args()}
                    ),
                    'normalize': True,
                    'normalize_args': Args(
                        args=('std',)
                        kwargs={'func': None, 'func_args': Args()}
                    ),
                    'pca': True,
                    'pca_args': Args(
                        args=(0.85, ),
                        kwargs={}
                    ),
                    'func': None,
                    'func_args': Args()
                }
            )
            ```

        Fortunately, the most arguments of member methods have been set to
        proper values by default.

        Further, this incredible module has provided the function `warp_args`
        to warp the flat argument array passed in.
        """
        self.y_label = y_label
        self.__estimator = estimator
        if read_args is None:
            read_args = Args()
        if preprocess_args is None:
            preprocess_args = Args()
        if isinstance(dataset, str):
            dataset = Path(dataset)
        if isinstance(dataset, Path):
            self.read_from = dataset
            self.read(*read_args.args, **read_args.kwargs)
            self.preprocess(*preprocess_args.args, **preprocess_args.kwargs)
        elif isinstance(dataset, pd.DataFrame):
            self.read_from = None
            self.__raw = dataset
            self.preprocess(*preprocess_args.args, **preprocess_args.kwargs)
        else:
            raise TypeError('Invalid type for argument `dataset`.')
        self.positive = positive

    def read(
        self: Self,
        *,
        func: Optional[Callable[..., pd.DataFrame]] = None,
        func_args: Optional[Args] = None
    ) -> Self:
        """
        HTML file may have an unpredictable structure, therefore, to make
        this method more concise, reading HTML is required to be implemented
        from outer scope.

        Parameters
        ----------
        func : Callable[..., pd.DataFrame], optional
            If not None, the Callable passed in will be called for
            the data retrieving.
        func_args : Args, optional
            Arguments for `func`.

        Raises
        ------
        FormatError
            Raise when file extension is invalid.
        """
        if func is not None:
            if func_args is None:
                func_args = Args()
            self.__raw = func(*func_args.args, **func_args.kwargs)
            return self
        assert self.read_from is not None
        extension: str = self.read_from.suffix.lower().lstrip('.')
        if extension == 'csv':
            self.__raw = pd.read_csv(self.read_from)
        elif extension == 'json':
            self.__raw = pd.read_json(self.read_from)
        elif extension  == 'xml':
            self.__raw = pd.read_xml(self.read_from)
        elif extension in ('xlsx', 'xls'):
            self.__raw = pd.read_excel(self.read_from)
        else:
            raise FormatError('Unknown dataset format.')
        return self

    @staticmethod
    def numerify(
        data: pd.DataFrame,
        by: Literal['codes', 'one-hot'] = 'codes',
        *,
        func: Optional[Callable[..., pd.DataFrame]] = None,
        func_args: Optional[Args] = None
    ) -> pd.DataFrame:
        """
        Convert categorical variables into numerical variables.

        Parameters
        ----------
        data : pd.DataFrame
            Data with categorical variables.
        by : Literal['codes', 'one-hot'], optional
                'codes' : Convert with `.cat.codes`.
                'one-hot' : Convert with `pd.get_dummies`.
            Determine how to convert categorical variables to numerical.
        func : Callable[..., pd.DataFrame], optional
            If not None, argument `by` will be omitted, and the Callable
            passed in will be called for the conversion.
        func_args : Args, optional
            Arguments for `func`.

        Returns
        -------
        pd.DataFrame
            Data that all variables are numerical.

        Raises
        ------
        ValueError
            Raise when the value of argument `by` is invalid.
        """
        if func is not None:
            if func_args is None:
                func_args = Args()
            return func(*func_args.args, **func_args.kwargs)
        if by == 'codes':
            cat = data.select_dtypes(exclude='number')
            return data.assign(**{
                label: pd.Categorical(col).codes
                for label, col in cat.items()  # `iteritems` is deprecated
            })
        elif by == 'one-hot':
            return pd.get_dummies(data)
        else:
            raise ValueError("Invalid value for argument `by`.")

    def __numerify(
        self: Self,
        by: Literal['codes', 'one-hot'] = 'codes',
        *,
        func: Optional[Callable[..., pd.DataFrame]] = None,
        func_args: Optional[Args] = None
    ) -> Self:
        assert self.__cache is not None
        self.__cache = self.numerify(
            self.__cache,
            by,
            func=func,
            func_args=func_args
        )
        return self

    @staticmethod
    def normalize(
        data: pd.DataFrame,
        by: Literal['std', 'max-min'] = 'std',
        *,
        func: Optional[Callable[..., pd.DataFrame]] = None,
        func_args: Optional[Args] = None
    ) -> pd.DataFrame:
        """
        Normalize data.

        Note that data passed in is assumed to be with no NaN value.

        Parameters
        ----------
        data : pd.DataFrame
            Data with categorical variables.
        by : Literal['std', 'max-min'], optional
                'std' : Standardization.
                'max-min' : Max-Min Normalization.
            Normalization type.
        func : Callable[..., pd.DataFrame], optional
            If not None, argument `by` will be omitted, and the Callable
            passed in will be called for the normalization.
        func_args : Args, optional
            Arguments for `func`.

        Returns
        -------
        pd.DataFrame
            Normalized data.

        Raises
        ------
        ValueError
            Raise when the value of argument `by` is invalid.
        """
        if func is not None:
            if func_args is None:
                func_args = Args()
            return func(*func_args.args, **func_args.kwargs)
        num = data.select_dtypes(include='number')
        if by == 'std':
            num = (num - num.mean()) / num.std()
        elif by == 'max-min':
            num = (num - num.min()) / (num.max() - num.min())
        else:
            raise ValueError("Invalid value for argument `by`.")
        return data.assign(**dict(num.items()))

    def __normalize(
        self: Self,
        by: Literal['std', 'max-min'] = 'std',
        *,
        func: Optional[Callable[..., pd.DataFrame]] = None,
        func_args: Optional[Args] = None
    ) -> Self:
        assert self.__cache is not None
        self.__cache = self.normalize(
            self.__cache,
            by,
            func=func,
            func_args=func_args
        )
        return self

    @staticmethod
    def pca(data: pd.DataFrame, info_ratio: float = 0.85) -> PCA_Result:
        """
        Parameters
        ----------
        data : pd.DataFrame
            Data to be PCA decomposited.
        info_ratio : float, optional
            PCA info ratio.

        Returns
        -------
        PCA_Result
            _description_
        """
        assert 0 <= info_ratio <= 1

        pca = PCA()
        pca.fit(data)
        summary = pd.DataFrame({
            'Standard deviation': np.sqrt(pca.explained_variance_),
            'Proportion of variance': pca.explained_variance_ratio_,
            'Cumulative proportion': np.cumsum(pca.explained_variance_ratio_)
        }).T
        summary.columns = (f'PC_{i + 1}' for i in range(summary.shape[1]))
        for i, j in enumerate(summary.loc['Cumulative proportion']):
            if j >= info_ratio:
                num_of_pc = i + 1
                break
        components = pd.DataFrame(
            pca.components_.T,
            columns=summary.columns,
            index=data.columns
        ).iloc[:, :num_of_pc]
        scores = pd.DataFrame(
            pca.transform(data),
            columns=summary.columns
        ).iloc[:, :num_of_pc]
        summary.round(4)
        return PCA_Result(summary, components, scores)

    def __pca(self: Self, info_ratio: float = 0.85) -> Self:
        assert self.__cache is not None
        self.__cache = self.pca(self.__cache, info_ratio).scores
        return self

    def preprocess(
        self: Self,
        *,
        dropna: bool = True,
        dropna_args: Optional[Args] = None,
        numerify: bool = True,
        numerify_args: Optional[Args] = None,
        normalize: bool = False,
        normalize_args: Optional[Args] = None,
        pca: bool = False,
        pca_args: Optional[Args] = None,
        func: Optional[Callable[..., pd.DataFrame]] = None,
        func_args: Optional[Args] = None
    ) -> Self:
        """
        Data prepocessing.

        Parameters
        ----------
        dropna : bool, optional
            If True, drop rows with NaN value.
        dropna_args : Optional[Args], optional
            Arguments for `pd.Dataframe.dropna`.
        numerify : bool, optional
            If True, convert categorical variables to numerical.
        numerify_args : Optional[Args], optional
            Arguments for `self.__numerify`.
        normalize : bool, optional
            If True, normalize data.
        normalize_args : Optional[Args], optional
            Arguments for `self.__normalize`.
        pca : bool, optional
            If True, PCA-decomposite data.
        pca_args : Optional[Args], optional
            Arguments for `self.__pca`.
        func : Optional[Callable[..., pd.DataFrame]], optional
            If not None, all other arguments except `func_args` will be
            omitted, and the Callable passed in will be called for
            preprocessing.
        func_args : Optional[Args], optional
            Arguments for `func`.
        """
        if func is not None:
            if func_args is None:
                func_args = Args()
            self.__data = func(*func_args.args, **func_args.kwargs)
            return self

        self.__cache = self.__raw.copy(deep=True)

        if dropna:
            if dropna_args is None:
                dropna_args = Args()
            temp = self.__cache.dropna(*dropna_args.args, **dropna_args.kwargs)
            if temp is not None:  # inplace == False
                self.__cache = temp

        self.__y = self.__cache[self.y_label].astype(str)
        self.__cache.drop(self.y_label, axis=1, inplace=True)

        if numerify:
            if numerify_args is None:
                numerify_args = Args()
            self.__numerify(*numerify_args.args, **numerify_args.kwargs)

        if normalize:
            if normalize_args is None:
                normalize_args = Args()
            self.__normalize(*normalize_args.args, **normalize_args.kwargs)

        if pca:
            if pca_args is None:
                pca_args = Args()
            self.__pca(*pca_args.args, **pca_args.kwargs)

        self.__data = self.__cache.copy(deep=True)

        return self

    @property
    def raw(self) -> pd.DataFrame:
        return self.__raw

    @property
    def data(self) -> pd.DataFrame:
        return self.__data

    @property
    def y(self) -> pd.Series:
        return self.__y

    @property
    def y_cat(self) -> pd.Categorical:
        return pd.Categorical(self.__y)

    @property
    def y_num(self) -> np.ndarray:
        return self.y_cat.codes

    @property
    def is_binary(self) -> bool:
        return True if len(self.__y.unique()) <= 2 else False

    @property
    def positive(self) ->Optional[str]:
        """Return class marked positive."""
        return self.__positive

    @positive.setter
    def positive(self, __value: Optional[str]) -> None:
        assert __value in self.__y.to_numpy() or __value is None
        self.__positive = __value

    @property
    def estimator(self) -> Estimator:
        return self.__estimator

    @estimator.setter
    def estimator(self, __value: Estimator) -> None:
        if self.__estimator is not None:
            input_ = input(
                f'Existing estimator `{self.__estimator}` will be destructed, '
                'this process is irreversible!\n'
                'Press `Y` + `Enter` to continue.\n'
                'Press any key else to stop.\n'
            )
            if input_.lower() != 'y':
                return print('Assigning process terminated.')
        self.__estimator = __value
        return print(f'Property `estimator` is now set to `{__value}`.')

    def show_doc(self, member: Optional[str] = None) -> None:
        if member is None:
            return print(self.__estimator.__doc__)
        return print(getattr(self.__estimator, member).__doc__)

    @overload
    @staticmethod
    def fit(
        X: pd.DataFrame,
        y: np.ndarray,
        estimator: Estimator,
        *args,
        **kwargs
    ) -> None:
        pass

    @overload
    @staticmethod
    def fit(
        X: pd.DataFrame,
        y: pd.Series,
        estimator: Estimator,
        *args,
        **kwargs
    ) -> None:
        pass

    @staticmethod
    def fit(X, y, estimator: Estimator, *args, **kwargs) -> None:
        """
        Fit data with given estimator instance.

        Parameters
        ----------
        X : pd.DataFrame
            Training data.
        y : np.ndarray | pd.Series
            Classes corresponding to training data.
        """
        estimator.fit(X, y, *args, **kwargs)

    @staticmethod
    def predict(
        X: pd.DataFrame,
        estimator: Estimator,
        *args,
        **kwargs
    ) -> np.ndarray:
        """
        Predict data with given estimator instance.

        Parameters
        ----------
        X : pd.DataFrame
            Testing data.

        Returns
        -------
        np.ndarray
            Classes predicted.
        """
        return estimator.predict(X, *args, **kwargs)

    def __results(self, y_pred: Iterable, y_test: Iterable):
        iter_pred = iter(y_pred)
        iter_test = iter(y_test)
        is_binary = self.is_binary
        while True:
            try:
                pred = next(iter_pred)
                test = next(iter_test)
            except StopIteration:
                break
            if is_binary:
                assert self.__positive is not None
                yield BoolTruthPair(
                    (pred == self.__positive),
                    (test == self.__positive)
                ).type_
            else:
                yield TruthPair(pred, test).type_

    def evaluate(
        self,
        test_size: float = 0.2,
        *,
        fit_args: Optional[Args] = None,
        predict_args: Optional[Args] = None,
        verbose: bool = True,
        return_: bool = False
    ) -> Optional[float]:
        """
        Evaluate `self.__estimator` performance.

        Parameters
        ----------
        test_size : float, optional
            Size of test set.
            See more in: 'https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split'
        fit_args : Args, optional
            Arguments for `self.fit`.
        predict_args : Args, optional
            Arguments for `self.predict`.
        verbose : bool, optional
            If True, display details.
        return_ : bool, optional
            If True, return accuracy.

        Returns
        -------
        Optional[float] :
            Accuracy.
        """
        assert self.__estimator is not None
        assert 0 < test_size < 1

        x_train, x_test, y_train, y_test = train_test_split(
            self.__data,
            self.__y
            # in current implementation,
            # I decide not to use `self.y_cat` and `self.y_num`
        )

        if fit_args is None:
            fit_args = Args()
        self.fit(
            x_train,
            y_train,
            self.__estimator,
            *fit_args.args,
            **fit_args.kwargs
        )

        if predict_args is None:
            predict_args = Args()
        y_pred: np.ndarray = self.predict(
            x_test,
            self.__estimator,
            *predict_args.args,
            **predict_args.kwargs
        )

        result = ConfusionMatix(self.__results(y_pred, y_test))

        if verbose:
            display(result)

        return result.accuracy if return_ else None

    def kfold_cv(
        self,
        n_splits: int = 5,
        *,
        shuffle: bool = False,
        random_state: Any = None,
        estimator_args: Optional[Args] = None,
        fit_args: Optional[Args] = None,
        predict_args: Optional[Args] = None,
        verbose: bool = True,
        return_: bool = False
    ) -> Optional[float]:
        """
        K-Fold cross-validation.
        See more in: 'https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold'

        Note that this method will NOT use `self.__estimator` but a set of
        new estimators instantiated from `self.__eatimator.__class__` that
        are initiated with the same arguments.

        Parameters
        ----------
        estimator_args : Args, optional
            Arguments for `self.__eatimator.__class__.__init__`.
        fit_args : Args, optional
            Arguments for `self.fit`.
        predict_args : Args, optional
            Arguments for `self.predict`.
        verbose : bool, optional
            If True, display details.
        return_ : bool, optional
            If True, return  average accuracy.

        Returns
        -------
        Optional[float] :
            Average accuracy.
        """
        assert self.__estimator is not None

        if verbose:
            display(HTML(f'<h2{n_splits}-Fold Cross-Validationtitle</h2>'))

        data = self.__data
        kfold = KFold(n_splits, shuffle=shuffle, random_state=random_state)

        if estimator_args is None:
            estimator_args = Args()
        if fit_args is None:
            fit_args = Args()
        if predict_args is None:
            predict_args = Args()

        stats = ConfusionMatix().statistics
        stats['value'] = 0  # NaN is infectious
        stats.index = 'average ' + stats.index

        # every iteration share the same arguments
        for i, (train_indices, test_indices) in enumerate(kfold.split(data)):
            x_train = data.iloc[train_indices]
            x_test = data.iloc[test_indices]
            y_train = self.__y[train_indices]
            y_test = self.__y[test_indices]
            estimator = type(self.__estimator)(
                *estimator_args.args,
                **estimator_args.kwargs
            )
            self.fit(
                x_train,
                y_train,
                estimator,
                *fit_args.args,
                **fit_args.kwargs
            )
            y_pred: np.ndarray = self.predict(
                x_test,
                estimator,
                *predict_args.args,
                **predict_args.kwargs
            )
            result = ConfusionMatix(self.__results(y_pred, y_test))
            if verbose:
                display(HTML(f'<h3>Iteration {i + 1}</h3>'))
                display(result)
            stats['value'] += result.statistics['value'].to_numpy()

        stats['value'] /= n_splits

        if verbose:
            display(HTML('<h3>Summary</h3>'))
            display(stats)

        return stats.loc['average accuracy', 'value'] if return_ else None

    def score(
        self,
        *,
        fit_args: Optional[Args] = None,
        predict_args: Optional[Args] = None,
    ) -> float:
        return self.kfold_cv(   # type: ignore
            fit_args=fit_args,
            predict_args=predict_args,
            verbose=False,
            return_=True
        )

    def _repr_html_(self) -> str:
        if self.read_from is None:
            source_info = 'DataFrame directly imported.'
        else:
            source_info = str(self.read_from.absolute())
        if self.__estimator is None:
            estimator_info = 'No estimator has been passed.'
        else:
            doc: str = self.__estimator.__doc__  # annotated for mypy
            doc_html = doc.replace('\n', '<br/>').replace(' ', '&nbsp;')
            estimator_info = f"""
                <details>
                    <summary>{self.__estimator.__class__.__name__}</summary>
                    <p>{doc_html}</p>
                </details>
            """
        return f"""
            <div>
                <h2>The Incredible Magic Class for IE7275 Project</h2>
                    <h3>Team Members</h3>
                        <p>
                            <span>Anqi Guo</span>,&nbsp;
                            <span>Junxiang Yang</span>,&nbsp;
                            <span>Lingxuan Ye</span>&nbsp;
                        </p>
                    <h3>Status</h3>
                        <h4>Data Info</h4>
                            <p><b>source</b>: {source_info}</p>
                            <p><b>y-label</b>: {self.y_label}</p>
                        <h4>Raw Data</h4>
                            <div>{self.__raw._repr_html_()}</div>
                        <h4>Processed Data</h4>
                            <div>{self.__data._repr_html_()}</div>
                        <h4>Estimator</h4>
                            <div>{estimator_info}</div>
            </div>
        """


def cast(
    dataset: Union[Path, str, pd.DataFrame],
    y_label: str,
    positive: Optional[str] = None,
    estimator: Optional[Estimator] = None,
    dropna: bool = True,
    numerify: bool = True,
    numerify_by: Literal['codes', 'one-hot'] = 'codes',
    normalize: bool = False,
    normalize_by: Literal['std', 'max-min'] = 'std',
    pca: bool = False,
    info_ratio: float = 0.85,
) -> Magic:
    """
    Factory function of `Magic`.

    Parameters
    ----------
    dataset : Path | str | pd.DataFrame
        Dataset source.
    y_label : str
        Determine which column is classification objective.
    positive : Optional[str], optional
        Mark specified class as positive.
    estimator : Estimator
        Estimator instance.
    dropna : bool, optional
        If True, drop rows with NaN value.
    numerify : bool, optional
        If True, convert categorical variables to numerical.
    numerify_by : Literal['codes', 'one-hot'], optional
            'codes' : Convert with `.cat.codes`.
            'one-hot' : Convert with `pd.get_dummies`.
        Determine how to convert categorical variables to numerical.
    normalize : bool, optional
        If True, normalize data.
    normalize_by : Literal['std', 'max-min'], optional
            'std' : Standardization.
            'max-min' : Max-Min Normalization.
        Normalization type.
    pca : bool, optional
        If True, PCA-decomposite data.
    info_ratio : float, optional
        PCA info ratio.

    Returns
    -------
    Magic
        `Magic` instance.
    """
    return Magic(
        dataset,  # type: ignore
        y_label,
        positive,
        estimator,
        preprocess_args=Args(
            kwargs={
                'dropna': dropna,
                'numerify': numerify,
                'numerify_args': Args(args=(numerify_by,)),
                'normalize': normalize,
                'normalize_args': Args(args=(normalize_by,)),
                'pca': pca,
                'pca_args': Args(args=(info_ratio,))
            }
        )
    )


def grid_search(
    dataset: Union[Path, str, pd.DataFrame],
    y_label: str,
    positive: Optional[str] = None,
    params: Optional[Dict[str, list]] = None,
    top_n: int = 1
) -> BestResult:
    if params is None:
        params = PARAMS
    grid = np.meshgrid(*params.values())
    combinations  = np.empty_like(grid[0], dtype=np.object_)
    scores = np.empty_like(grid[0], dtype=np.float_)
    for index, estimator_type in np.ndenumerate(grid[0]):
        estimator = estimator_type()
        combination = (estimator_type, *(i[index] for i in grid[1:]))
        if not any(index):  # (0, 0, ...)
            inst = cast(
                dataset,
                y_label,
                positive,
                estimator,
                *combination[1:]
            )
            raw = inst.raw  # to save memory and aviod large volume IO
        else:
            inst = cast(raw, y_label, positive, estimator, *combination[1:])
        combinations[index] = combination
        scores[index] = inst.score()
    top_n = min(top_n, grid[0].size)
    top_n_indices = scores.argsort(axis=None)[::-1][:top_n]
    return BestResult(
        combinations.flatten()[top_n_indices],
        scores.flatten()[top_n_indices]
    )
