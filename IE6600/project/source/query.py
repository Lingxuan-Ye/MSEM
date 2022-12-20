"""
Only available when the current working directory
is the root of this project.

This module is full of HARD CODING, please:

1. DO NOT LEARN CODING NORM FROM THIS MODULE!
2. DO NOT LEARN CODING NORM FROM THIS MODULE!!
3. DO NOT LEARN CODING NORM FROM THIS MODULE!!!
"""

import json
from typing import Dict, Tuple

import pandas as pd

from .io_ import IO

GENERAL = ['state', 'population', 'LandArea']
ECO = ['medIncome', 'PctPopUnderPov', 'PctUnemployed']
# RACE = ['racepctblack', 'racePctWhite', 'racePctAsian', 'racePctHisp']
HOMELESS = ['NumInShelters', 'NumStreet']
SECURITY = ['LemasPctOfficDrugUn', 'ViolentCrimesPerPop']

COLUMNS = [*GENERAL, *ECO, *HOMELESS, *SECURITY]


class Query:

    def __init__(self) -> None:
        with open('./_data/us-states.json') as f:
            geojson = json.load(f)

        # str is Iterable as well
        io = IO(as_NaN='?')  # type: ignore # stupid mypy
        io.set_raw(
            pd.merge(
                pd.read_csv(
                    './_data/state_fips_master.csv'
                )[['fips', 'state_name', 'state_abbr']],
                io.raw[COLUMNS].rename({'state': 'fips'}, axis=1)
            ),
            force=True
        ).preprocess()
        data = io.data
        group = data.groupby('fips')
        first = group.first()

        self.__available = (
            'population',
            'population_density',
            'median_income',
            'percent_of_population_under_poverty',
            'percent_of_unemployed',
            'percent_of_homeless',
            'percent_of_officers_assigned_to_drug_units',
            'violent_crime_density'
        )
        self.__attr_info = io.attr_info
        self.__geojson = geojson
        self.__data = data
        self.__group = group
        self.__fips = first.index.map(lambda x: f'{x:02}')
        self.__state_name = first['state_name']
        self.__state_abbr = first['state_abbr']
        self.__a = pd.Series(index=range(len(self.__fips)), dtype=float)
        self.__cache: Dict[str, pd.Series] = {}

    @staticmethod
    def normalize(x: pd.Series) -> pd.Series:
        """
        Max-Min Normalization.
        """
        return (x - x.min()) / (x.max() - x.min())

    @staticmethod
    def scale(x: pd.Series) -> pd.Series:
        """
        Proportionally map values to (0, 1].
        """
        return x / x.max()

    @property
    def available(self) -> Tuple[str, ...]:
        return self.__available

    @property
    def attr_info(self) -> pd.DataFrame:
        return self.__attr_info

    @property
    def geojson(self) -> str:
        return self.__geojson

    @property
    def data(self) -> pd.DataFrame:
        return self.__data

    @property
    def fips(self) -> pd.Index:
        return self.__fips

    @property
    def state_name(self) -> pd.Series:
        return self.__state_name

    @property
    def state_abbr(self) -> pd.Series:
        return self.__state_abbr

    # Warning
    # -------
    # Every property-decorated methods from the first one below
    # are COMPLETELY WRONG:

    # Max-Min-scaled column values are NO LONGER linear (propotional) unless
    # every minimum values in each column are always zero, which is of no
    # chance to be true.

    # This kind of nonlinear relationship came from the original data
    # passed in for it was scaled by Max-Min normalization.

    # In general, every results below are invalid for the data has
    # already degenerated from ratio to ordinal at the very beginning.

    # Hope no one would read my source and see my comments.

    @property
    def population(self) -> pd.Series:
        if self.__cache.get('population') is None:
            self.__cache['population'] = self.scale(
                self.__group['population'].sum()
            )
        return self.__cache['population']

    @property
    def population_density(self) -> pd.Series:
        if self.__cache.get('population_density') is None:
            self.__cache['population_density'] = self.scale(
                self.__group['population'].sum() \
                / self.__group['LandArea'].sum()
            )
        return self.__cache['population_density']

    @property
    def median_income(self) -> pd.Series:
        if self.__cache.get('median_income') is None:
            for i, (_, v) in enumerate(self.__group):
                pop = v['population']
                half_pop = pop.sum() / 2
                order = pop.sort_values().index
                for j, k in enumerate(pop[order].cumsum()):
                    if k > half_pop:
                        self.__a[i] = v.loc[order[j], 'medIncome']
            self.__cache['median_income'] = self.scale(self.__a)
        return self.__cache['median_income']

    @property
    def percent_of_population_under_poverty(self) -> pd.Series:
        if self.__cache.get('percent_of_population_under_poverty') is None:
            for i, (_, v) in enumerate(self.__group):
                pop = v['population']
                self.__a[i] = (v['PctPopUnderPov'] * pop).sum() / pop.sum()
            self.__cache[
                'percent_of_population_under_poverty'
            ] = self.scale(self.__a)
        return self.__cache['percent_of_population_under_poverty']

    @property
    def percent_of_unemployed(self) -> pd.Series:
        """
        This assumes each county has the same proportion of people
        that are 16 and over.
        """
        if self.__cache.get('percent_of_unemployed') is None:
            for i, (_, v) in enumerate(self.__group):
                pop = v['population']
                self.__a[i] = (v['PctUnemployed'] * pop).sum() / pop.sum()
            self.__cache['percent_of_unemployed'] = self.scale(self.__a)
        return self.__cache['percent_of_unemployed']

    @property
    def percent_of_homeless(self) -> pd.Series:
        if self.__cache.get('percent_of_homeless') is None:
            for i, (_, v) in enumerate(self.__group):
                pop = v['population']
                homeless = v['NumInShelters'] + v['NumStreet']
                self.__a[i] = homeless.sum() / pop.sum()
            self.__cache['percent_of_homeless'] = self.scale(self.__a)
        return self.__cache['percent_of_homeless']

    @property
    def percent_of_officers_assigned_to_drug_units(self) -> pd.Series:
        """
        This assumes the ratios of police officers to population
        in every counties are the same which is most likely to be wrong.
        """
        if self.__cache.get(
            'percent_of_officers_assigned_to_drug_units'
        ) is None:
            for i, (_, v) in enumerate(self.__group):
                pop = v['population']
                self.__a[i] = (v['LemasPctOfficDrugUn'] * pop).sum() / pop.sum()
            self.__cache[
                'percent_of_officers_assigned_to_drug_units'
            ] = self.scale(self.__a)
        return self.__cache['percent_of_officers_assigned_to_drug_units']

    @property
    def violent_crime_density(self) -> pd.Series:
        if self.__cache.get('violent_crime_density') is None:
            for i, (_, v) in enumerate(self.__group):
                crime = v['ViolentCrimesPerPop']
                pop = v['population']
                area = v['LandArea']
                self.__a[i] = ((crime * pop).sum() / area.sum())
            self.__cache['violent_crime_density'] = self.scale(self.__a)
        return self.__cache['violent_crime_density']
