# CovidHub

![commit activity](https://img.shields.io/github/commit-activity/m/kenticent9/corbot_ua) ![last commit](https://img.shields.io/github/last-commit/kenticent9/corbot_ua)

This is a repository for mini-projects about COVID-19: EpidemLab, Corbot and Cormap, which 
* simulate the spread of the disease with your parameters
* keep you updated with the daily coronavirus situation in a country you choose, build comparison plots
* display the current coronavirus situation around the globe 

respectively. It was created as a semester work from the programming basics course of the two students of Ukrainian Catholic University.

## EpidemLab

![EpidemLab version](https://img.shields.io/badge/version-1.0-informational)

This application simulates a disease spread with you parameters. It is simple yet versatile and effectively shows and visualizes the dependency of the spread of a disease on its parameters and mitigation measures.

### Example

With quarantine

![with_q](https://github.com/kenticent9/corbot_ua/blob/master/images/with_q.gif)

No quarantine

![no_q](https://github.com/kenticent9/corbot_ua/blob/master/images/no_q.gif)

### Guide

In summary, there are 13 parameters, 10 of which you can enter by yourself.

Disease:
* Infection rate: float [0, 1] - chance of infected cell infecting its neighbour
* Serial interval: int [0, inf) - how fast the disease spreads
* Contagious period: int [0, inf) - how long the cell is contagious
* Fatality: float [0, 1] - the chance of infected cell dying when the contagious period ends
* Immunity: float [0, 1] - the chance of healthy cell not being reinfected

Quarantine:
* Quarantine introduced: int [0, inf) - the day on which the quarantine is introduced
* Quarantine effectiveness: float [0, 1] - the chance of infected cell being found and put on quarantine forever

Medication:
* Medication invented: int [0, inf) - the day on which the medicine is invented
* Medication effectiveness: float [0, 1] - the chance of infected cell recovering after taking the medicine

Simulation:
* Filename: str - the file's name in which the results of the simulation will be saved
* Number of days: int - how long the simulation lasts (can't be entered)
* Width: int - the number of cells on each side of the grid (can't be entered)
* Population density: int - the percentage of board covered with cells (can't be entered)

The last three parameters cannot be entered by the user, because they proved themselves to be optimal and there's little sense in changing them, but if you want, you can do it by editing the code.

## Corbot

![Corbot version](https://img.shields.io/badge/version-1.0-informational)

![plot](https://github.com/kenticent9/corbot_ua/blob/master/images/bot.png)

## Map

![Map version](https://img.shields.io/badge/version-1.1-informational)

![map](https://github.com/kenticent9/corbot_ua/blob/master/images/map.png)
