from country import Country
from json import load
import folium


def get_sum_countries():
    countries = set()
    with open('data/summary.json', 'r', encoding='UTF-8') as f:
        sum_data = load(f)
    for cntry in sum_data['Countries']:
        try:
            cur_cntry = Country(cntry['Country'], cntry['CountryCode'])
            cur_cntry.add_day(cntry['Date'], cntry['TotalConfirmed'],
                              cntry['TotalDeaths'], cntry['TotalRecovered'])
            cur_cntry.set_total()
            countries.add(cur_cntry)
        except KeyError as e:
            print(e)
    return countries


def get_sum_confirmed(countries):
    confirmed = {}
    for cntry in countries:
        confirmed[cntry._name] = cntry._confirmed
    return confirmed


def create_map(countries):
    sum_map = folium.Map()
    confirmed_fg = folium.FeatureGroup()
    # confirmed_fg.add_child(folium.GeoJson(data=open('borders.json', 'r').read(), style_function=lambda x: {'fillColor': ''}))
    for cntry in countries:
        folium.CircleMarker(
            location=cntry._coordinates,
            radius=0.0001*cntry._confirmed,
            popup=cntry._name,
            color='red',
            fill=True,
            fill_color='#3186cc'
        ).add_to(sum_map)
    sum_map.save('sum_map.html')


def main():
    countries = get_sum_countries()
    confirmed = get_sum_confirmed(countries)
    create_map(countries)


if __name__ == '__main__':
    main()
