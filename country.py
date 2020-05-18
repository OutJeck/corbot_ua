import country_converter as coco
import pandas as pd


class Country:
    cc = coco.CountryConverter()
    df = pd.read_csv('data/population.csv', index_col=1, skiprows=4)
    df = df['2018']

    def __init__(self, iso2, confirmed):
        self._name = Country.cc.convert(iso2, to='name_short')
        self._iso3 = Country.cc.convert(iso2)
        self._confirmed = confirmed
        self._cpm = self._calculate_cpm(Country.df[self._iso3])
        self._days = {}

    def _calculate_cpm(self, population):
        return (self._confirmed/population) * 1000000

    @property
    def iso3(self):
        return self._iso3

    @property
    def cpm(self):
        return self._cpm

    def __repr__(self):
        return f"Name: {self._name}\nISO 3: {self._iso3}\n" \
               f"Confirmed: {self._confirmed}\nCPM: {self._cpm}"

    def __str__(self):
        return self._name


if __name__ == '__main__':
    pass
