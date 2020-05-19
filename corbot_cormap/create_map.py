import folium

from corbot_cormap.country import Country
from corbot_cormap.get_data import load_data

from folium.plugins import FloatImage

# Create a map object
sum_map = folium.Map(tiles='cartodbdark_matter', location=[0, 0], zoom_start=2)

borders = load_data('borders')

sum_data = load_data('summary')
countries = []
for cntry in sum_data['Countries']:
    try:
        countries.append(
            Country(cntry['CountryCode'], cntry['TotalConfirmed']))
    except KeyError as e:
        print(e)
countries = list(map(lambda x: (x.iso3, x.cpm), countries))

# Display the choropleth map
choropleth = folium.Choropleth(
    geo_data=borders,
    data=countries,
    key_on='feature.id',
    bins=[0] + [156.25 * 2**i for i in range(8)],
    fill_color='YlOrRd',
    fill_opacity=1,
    smooth_factor=0,
    highlight=True
).add_to(sum_map)

# Delete the legend of the choropleth
for key in choropleth._children:
    if key.startswith('color_map'):
        del choropleth._children[key]

# Display image legend
legend = 'https://i.imgur.com/axMZjuk.png'
FloatImage(legend, bottom=17, left=94).add_to(sum_map)

# Display the name of the countries
style_function = 'font-size: 15px; font-weight: bold'
choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['name'], style=style_function, labels=False))

sum_map.save('website/templates/sum_map.html')
