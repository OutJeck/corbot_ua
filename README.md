# CovidHub

This project regarding COVID-19 consists of 3 parts:

## EpidemLab

This is an application for simulating a disease spread with you parameters.

### Example

With quarantine

![with_q](https://github.com/kenticent9/corbot_ua/blob/master/images/with_q.gif)

No quarantine

![no_q](https://github.com/kenticent9/corbot_ua/blob/master/images/no_q.gif)

### Guide

In summary, there are 13 parameters of the simulation, 10 of which you can enter by yourself.

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
* Number of days
* Width
* Density

## Corbot

![plot](https://github.com/kenticent9/corbot_ua/blob/master/images/bot.png)

## Map

![map](https://github.com/kenticent9/corbot_ua/blob/master/images/map.png)
