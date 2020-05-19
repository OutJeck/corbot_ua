import matplotlib.pyplot as plt
import pandas as pd

CHOICES = {"1": "infections",
           "2": "dead",
           "3": "recovered",
           "4": "infected"}

filenames = []
user_input = input("Enter the names of the files you want to compare without "
                   "the csv extension one by line. Press Enter to exit.\n> ")
while user_input:
    filenames.append(user_input)
    user_input = input("> ")

choice = CHOICES[input("Enter the number of stat you want to compare by:\n1. "
                       "Infections\n2. Dead\n3. Recovered\n4. Infected\n> ")]

dfs = []
for filename in filenames:
    dfs.append(pd.read_csv(f"data/{filename}.csv"))
for df, filename in zip(dfs, filenames):
    plt.plot(df[choice], label=filename)
plt.title(choice)
plt.legend()
plt.show()
