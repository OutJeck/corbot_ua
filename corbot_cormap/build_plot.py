import country_converter as coco
import matplotlib.pyplot as plt
from corbot_cormap.country import Country


def create_plot(country1, country2):
    CC = coco.CountryConverter()

    country_1 = Country(CC.convert(country1, to='ISO2'))
    country_2 = Country(CC.convert(country2, to='ISO2'))

    confirmed_1 = country_1.df['Confirmed']
    confirmed_2 = country_2.df['Confirmed']

    plt.figure()
    plt.plot(confirmed_1, '-', confirmed_2, '-')
    plt.xlabel("Date")
    plt.ylabel("Confirmed")
    plt.title("Confirmed over time")
    plt.legend([country1, country2])
    plt.savefig('telegram_plot_data/plot_png.png')
