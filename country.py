from collections import namedtuple

import pandas as pd


class Country:
    DF = pd.read_csv('data/coordinates.csv', index_col=0, keep_default_na=False)

    def __init__(self, name, code):
        # General info
        self._name = name
        self._code = code
        the_country = Country.DF.loc[code]
        self._coordinates = tuple(the_country[['latitude', 'longitude']])
        # COVID-19-related info
        self._days = {}
        self._confirmed = 0
        self._deaths = 0
        self._recovered = 0

    def add_day(self, date, confirmed, deaths, recovered):
        day = namedtuple('day', ['confirmed', 'deaths', 'recovered'])
        self._days[date] = day(confirmed, deaths, recovered)

    def set_total(self):
        self._confirmed, self._deaths, self._recovered \
            = list(self._days.values())[-1]

    def __repr__(self):
        return f"'Country': '{self._name}', 'CountryCode': {self._code}, " \
               f"'Coordinates': {self._coordinates}"
