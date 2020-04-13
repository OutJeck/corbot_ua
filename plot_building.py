import matplotlib.pyplot as plt

from data_processing import get_data, read_data, write_data


# Get data in json format about the two following countries
ua = get_data("ukraine").json()
pl = get_data("poland").json()

# Write it to json files for future use
write_data(ua, "data/ua.json")
write_data(pl, "data/pl.json")

# Build plot
cases_ua = [day['Cases'] for day in ua]
cases_pl = [day['Cases'] for day in pl]
dates_ua = [day['Date'][5:10] for day in ua]
dates_pl = [day['Date'][5:10] for day in pl]
plt.plot(dates_ua, cases_ua, label="Ukraine")
plt.plot(dates_pl, cases_pl, label="Poland")
plt.xticks(dates_ua, rotation='vertical')
plt.xticks(dates_pl, rotation='vertical')
plt.title("COVID-19 Ukraine-Poland Comparison")
plt.ylabel("Cases")
plt.xlabel("Date")
plt.legend()
plt.show()
