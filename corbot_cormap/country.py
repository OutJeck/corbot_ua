import country_converter as coco
import pandas as pd

from corbot_cormap.get_data import get_day_one_data


class Country:
    CC = coco.CountryConverter()
    DF = pd.read_csv('data/population.csv', index_col=1, skiprows=4)
    DF = DF['2018']

    def __init__(self, iso2, confirmed=0):
        self._name = Country.CC.convert(iso2, to='name_short')
        self._iso3 = Country.CC.convert(iso2)
        if confirmed == 0:
            self._df = self._get_df()
            self._R0 = self._calculate_R0()
        else:
            self._confirmed = confirmed
            self._population = Country.DF[self._iso3]
            self._cpm = self._calculate_cpm()

    def _calculate_cpm(self):
        return (self._confirmed/self._population) * 1000000

    def _get_df(self):
        get_day_one_data(self._name)
        df = pd.read_json(f'data/{self._name}.json')
        df = df.set_index('Date')
        df = df[['Confirmed', 'Deaths', 'Recovered']]
        return df

    def _calculate_R0(self):
        df = self._df
        new = df.iloc[-1]['Confirmed']
        existing = df.iloc[-2]['Confirmed']
        R0 = new / existing
        return R0

    def get_future(self, days):
        df = self._df
        R0 = self._R0
        cur_date = df.index[-1]
        for day in range(days):
            existing = df.loc[cur_date]['Confirmed']
            cur_date += pd.Timedelta(days=1)
            new = existing * R0
            df.loc[cur_date] = [new, None, None]
            print(cur_date, new)
        return df

    @property
    def iso3(self):
        return self._iso3

    @property
    def df(self):
        return self._df

    @property
    def confirmed(self):
        return self._confirmed

    @property
    def population(self):
        return self._population

    @property
    def cpm(self):
        return self._cpm

    def __repr__(self):
        return self._iso3

    def __str__(self):
        return self._name


if __name__ == '__main__':
    ua = Country('UA')
    print(ua.get_future(20))
    print(ua.df)
