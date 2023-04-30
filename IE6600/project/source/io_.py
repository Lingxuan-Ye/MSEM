import re
from pathlib import Path
from typing import Iterable, List, Optional, TypeVar, overload

import pandas as pd
from IPython.display import HTML

TAB = '&nbsp;' * 4

# `Self` is not supported until Python 3.11
# return `self` for method chaining
Self = TypeVar('Self', bound='IO')


class LoadingError(Exception):
    pass


class IO:

    DEFAULT_DIR = Path('./_data/')

    data_dir: Path
    as_NaN: List[str]

    __raw: pd.DataFrame
    __cache: pd.DataFrame
    __data: pd.DataFrame
    __attr_info: Optional[pd.DataFrame] = None

    @overload
    def __init__(
        self,
        data_dir: Optional[Path],
        as_NaN: Optional[Iterable[str]]
    ) -> None:
        pass

    @overload
    def __init__(
        self,
        data_dir: Optional[str],
        as_NaN: Optional[Iterable[str]]
    ) -> None:
        pass

    def __init__(
        self,
        data_dir=None,
        as_NaN=None
    ) -> None:
        if data_dir is None:
            # available when the current working directory
            # is the root of this project,
            # or directory under 'self.DEFAULT_DIR' does exist.
            data_dir = self.DEFAULT_DIR
        if isinstance(data_dir, str):
            data_dir = Path(data_dir)
        if not data_dir.is_dir():
            raise ValueError(f"Path '{data_dir}' is not a directory.")
        if as_NaN is None:
            as_NaN = []
        else:
            as_NaN = [i for i in as_NaN if isinstance(i, str)]
        self.data_dir = data_dir
        self.as_NaN = as_NaN
        self.read()

    def set_raw(
        self: Self,
        value: pd.DataFrame,
        force: bool = False
    ) -> Self:
        if not isinstance(value, pd.DataFrame):
            try:
                value = pd.DataFrame(value)
            except:
                raise ValueError('Invalid value for argument `__value`.')
        if not force:
            if input("Press 'Y' + 'Enter' to continue...").upper() != 'Y':
                print('Error: Action denied.')
                return self
            else:
                print('Succuess: Raw data has been replaced.')
        self.__raw = value
        self.__data = None

        return self

    @property
    def raw(self) -> pd.DataFrame:
        return self.__raw

    @raw.setter
    def raw(self, __value: pd.DataFrame) -> None:
        self.set_raw(__value)

    @property
    def data(self) -> pd.DataFrame:
        return self.__data

    @property
    def invalid_count(self) -> pd.DataFrame:
        count = self.__raw[self.__raw.isin(self.as_NaN)].count()
        return pd.DataFrame({'Attribute': count.index, 'Invalid': count.values})

    @property
    def attr_info(self) -> Optional[pd.DataFrame]:
        return self.__attr_info

    @property
    def inspection(self) -> HTML:
        if self.__attr_info is None:
            table = self.invalid_count
        else:
            table = pd.merge(
                self.invalid_count,
                self.__attr_info,
                on='Attribute'
            )
        return HTML(
            f"""
            <details>
                <summary>Attribute Inspection</summary>
                {table.to_html()}
            </details>
            """
        )

    def read(self: Self) -> Self:
        names_path: Optional[Path]= None
        data_path: Optional[Path]= None

        for i in self.data_dir.iterdir():
            if i.is_file():
                suffix = i.suffix.lower()
                if suffix == '.names':
                    if names_path is None:
                        names_path = i
                    else:
                        LoadingError('Multiple `.names` files exist.')
                elif suffix == '.data':
                    if data_path is None:
                        data_path = i
                    else:
                        LoadingError('Multiple `.data` files exist.')

        # assertion below is just for mypy for its stupidity
        assert names_path is not None and data_path is not None

        with open(names_path) as f:
            content = f.read()

        match = re.search(
            r'Attribute Information:\n.+(?=\nSummary Statistics:)',
            content,
            re.DOTALL
        )

        if match is not None:
            match = re.search(r'(?<=\n)--.+', match.group(), re.DOTALL)
            assert match is not None
            attr_info_content = match.group()
            names = re.findall(r'(?<=--\s).+?(?=:)', attr_info_content)
            infos = re.findall(r'(?<=:\s).+', attr_info_content)
            self.__attr_info = pd.DataFrame(
                data={'Attribute': names, 'Information': infos}
            )

        self.__raw = pd.read_csv(
            data_path,
            # consider that attribute order in 'Attribute Infomation
            # may not correspond with the data column order
            names=re.findall(r'(?<=@attribute\s)\S+', content)
        )
        self.__cache = self.__raw.copy()
        self.__data = self.__raw.copy()
        return self

    def reset_cache(self: Self) -> Self:
        self.__cache = self.__raw.copy()
        return self

    def expose(self: Self, write_data: bool = True) -> Self:
        """Convert invalid value to `NaN`."""
        self.__cache[self.__cache.isin(self.as_NaN)] = float('NaN')
        if write_data:
            self.__data = self.__cache.copy()
        return self

    def dropna(self: Self, write_data: bool = True) -> Self:
        """Drop rows with `NaN` value"""
        self.__cache.dropna(inplace=True)
        if write_data:
            self.__data = self.__cache.copy()
        return self

    def numerify(self: Self, write_data: bool = True) -> Self:
        """Convert number-like string to numeric."""
        cat = self.__cache.select_dtypes(exclude='number')
        self.__cache = self.__cache.assign(**{
            label: pd.to_numeric(col, errors='ignore')
            for label, col in cat.items()
        })
        assert isinstance(self.__cache, pd.DataFrame)
        if write_data:
            self.__data = self.__cache.copy()
        return self

    def preprocess(self: Self) -> Self:
        return self.reset_cache().expose(False).dropna(False).numerify(True)

    def _repr_html_(self) -> str:
        # note that `to_html` is different with `_repr_html_`
        # the former one returns a HTML string representing the whole data
        return f"""
            <div>
                <h2>Source</h2>
                    <p>{TAB}{self.data_dir.absolute()}</p>
                <h2>Data</h2>
                    <div>{self.__data._repr_html_()}</div>
            </div>
        """
