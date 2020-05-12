from country import Country
from get_data import load_data
import numpy as np
import matplotlib as mlp
import matplotlib.pyplot as plt


days = load_data("ukraine")
confirmed = [day['Confirmed'] for day in days]

plt.figure()
plt.plot(confirmed, '-')
plt.xlabel("Date")
plt.ylabel("Confirmed")
plt.title("Ukraine")
plt.show()
