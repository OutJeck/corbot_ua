"""Based on the material from towardsdatascience.com."""
import random
import tkinter as tk

# Colors
BLACK = '#000000'
RED = '#FF0000'
ORANGE = '#FFCC99'
GREEN = '#00FF00'
BLUE = '#99CCFF'
WHITE = '#FFFFFF'


class Cell:
    def __init__(self, x, y, color, grid, canvas):
        self.infected = False
        self.infected_once = False
        self.serial = 0  # Serial interval - how fast the disease spread from
        # one person to the next
        self.contagious = 0  # Contagious period
        self.immunity = 0  # Chance of reinfection

        self.medicated = False
        self.quarantined = False

        # Coordinates of the cell on the canvas, previously multiplied by 12
        self.x = x
        self.y = y

        self.color = color
        self.grid = grid
        self.canvas = canvas
        self.draw()
        self.grid.num += 1

    def draw(self):
        self.canvas.create_oval(self.x, self.y, self.x+10, self.y+10,
                                fill=self.color)

    def infect(self):
        self.color = ORANGE
        self.draw()
        self.infected = True
        self.serial = self.grid.SERIAL
        self.contagious = self.grid.CONTAGIOUS
        self.grid.num_infections += 1
        self.grid.cur_infected += 1
        if not self.infected_once:
            self.infected_once = True
            self.grid.num_infected += 1

    def recover(self):
        self.color = GREEN
        self.draw()
        self.infected = False
        self.serial = 0
        self.contagious = 0
        self.immunity = self.grid.IMMUNITY
        self.grid.num_recovered += 1
        self.grid.cur_infected -= 1

    def die(self):
        self.color = BLACK
        self.draw()
        self.infected = False
        self.grid.num_dead += 1
        self.grid.cur_infected -= 1

    def quarantine(self):
        self.color = BLUE
        self.draw()
        self.quarantined = True

    def medicate(self):
        if random.random() < self.grid.MED_EFFECTIVENESS:
            self.recover()
        else:
            self.medicated = True

    def process(self):
        if self.serial > 0:
            self.serial -= 1
        else:
            self.color = RED
            self.draw()
            if self.contagious > 0:
                self.contagious -= 1
            else:
                if random.random() > self.grid.FATALITY:
                    self.recover()
                else:
                    self.die()


class Simulation:
    def __init__(self, application):
        # Simulation
        self.WIDTH = 57
        self.DAYS = 200
        self.FILENAME = "untitled.csv"
        # Disease
        self.RATE = 0.25
        self.SERIAL = 3
        self.CONTAGIOUS = 9
        self.DENSITY = 0.7
        self.FATALITY = 0.07
        self.IMMUNITY = 0.5
        # Mitigation measures
        self.MED_INVENTED = 0
        self.MED_EFFECTIVENESS = 0
        self.Q_INTRODUCED = 50
        self.Q_EFFECTIVENESS = 0.2
        # Stats
        self.num_infections = 0
        self.num_recovered = 0
        self.num_dead = 0
        self.cur_infected = 0
        self.num_infected = 0
        self.num = 0

        self.application = application
        self.canvas = application.canvas
        self.grid = [[Cell(i*10, j*10, GREEN, self, self.canvas)
                      if random.random() < self.DENSITY
                      else Cell(i*10, j*10, BLACK, self, self.canvas)
                      for i in range(self.WIDTH)] for j in range(self.WIDTH)]
        self.canvas.update()

    def get_stats(self):
        try:
            ratio = self.num_recovered/self.num_infections * 100
        except ZeroDivisionError:
            ratio = 0
        return """Current infected: {} cells
Infected: {} out of {} ({:.2f}%)
Died: {} out of {} ({:.2f}%)
Recovered: {} out of {} ({:.2f}%)""".format(self.cur_infected,
                                            self.num_infected, self.num,
                                            self.num_infected/self.num*100,
                                            self.num_dead, self.num,
                                            self.num_dead/self.num*100,
                                            self.num_recovered,
                                            self.num_infections, ratio)

    def get_params(self):
        return """DISEASE
Infection rate: {:.2f}%
Serial interval: {} days
Contagious period: {} days
Fatality: {:.2f}%
Immunity: {:.2f}%

QUARANTINE
Quarantine introduced: {}th day
Quarantine effectiveness: {:.2f}%

MEDICINE
Medicine invented: {}th day
Medicine effectiveness: {:.2f}%""".format(self.RATE * 100,
                                          self.SERIAL,
                                          self.CONTAGIOUS,
                                          self.FATALITY * 100,
                                          self.IMMUNITY * 100,
                                          self.Q_INTRODUCED,
                                          self.Q_EFFECTIVENESS * 100,
                                          self.MED_INVENTED,
                                          self.MED_EFFECTIVENESS * 100)

    def infect_middle_cell(self):
        i = j = self.WIDTH // 2
        self.grid[i][j].infect()

    def get_coords_neighs(self, x, y):
        return [(i, j) for i in range(x-1, x+2) for j in range(y-1, y+2)
                if (i!=x or j!=y) and 0<=i<self.WIDTH and 0<=j<self.WIDTH]

    def main(self):
        f = open(f'data/{self.FILENAME}', 'w', encoding='UTF-8')
        f.write("infections,dead,recovered,infected\n")
        self.application.params.set(self.get_params())
        self.infect_middle_cell()

        for day in range(self.DAYS):
            f.write(f"{self.num_infections},{self.num_dead},"
                    f"{self.num_recovered},{self.num_infected}\n")
            self.application.day.set(f"Day: {day}/200")
            self.application.stats.set(self.get_stats())
            self.application.window.update()
            self.canvas.delete('all')

            for i in range(self.WIDTH):
                for j in range(self.WIDTH):
                    cur_cell = self.grid[i][j]
                    cur_cell.draw()
                    if cur_cell.color == BLACK or not cur_cell.infected:
                        continue
                    cur_cell.process()
                    if not cur_cell.infected or cur_cell.serial > 0:
                        continue
                    if not cur_cell.medicated and day > self.MED_INVENTED:
                        cur_cell.medicate()
                    if not cur_cell.infected:
                        continue
                    if not cur_cell.quarantined and day > self.Q_INTRODUCED \
                            and random.random() < self.Q_EFFECTIVENESS:
                        cur_cell.quarantine()
                    if not cur_cell.quarantined:
                        coords_neighs = self.get_coords_neighs(i, j)
                        for p, q in coords_neighs:
                            cur_neigh = self.grid[p][q]
                            if cur_neigh.color == BLACK or cur_neigh.infected:
                                continue
                            if random.random() > self.IMMUNITY:
                                if random.random() < self.RATE:
                                    cur_neigh.infect()
        f.close()


class Application:
    def __init__(self):
        self.window = tk.Tk()
        self.window.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))
        self.window.title("EpidemLab")

        self.canvas = tk.Canvas(self.window, height=561, width=561, bg=BLACK,
                                bd=10, relief=tk.SUNKEN, highlightthickness=0)
        self.simulation = Simulation(self)
        self.canvas.grid(row=0, column=0, rowspan=3, columnspan=3)

        self.day = tk.StringVar()
        self.day.set("Day: 0/200")
        self.day_label = tk.Label(self.window, textvariable=self.day,
                                  font='consolas', bg=BLACK, fg='white',
                                  justify=tk.LEFT, padx=10, pady=6,
                                  anchor='nw', highlightthickness=0)
        self.day_label.grid(row=0, column=3, columnspan=2, sticky=tk.NSEW)

        self.stats = tk.StringVar()
        self.stats.set(self.simulation.get_stats())
        self.stats_label = tk.Label(self.window, textvariable=self.stats,
                                    font='consolas', bg=BLACK, fg='white',
                                    justify=tk.LEFT,  width=39, padx=10,
                                    anchor='nw', highlightthickness=0)
        self.stats_label.grid(row=1, column=3, columnspan=2, sticky=tk.NSEW)

        self.params = tk.StringVar()
        self.params.set(self.simulation.get_params())
        self.params_label = tk.Label(self.window,
                                     textvariable=self.params,
                                     font='consolas', bg=BLACK, fg='white',
                                     justify=tk.LEFT, padx=10,
                                     anchor='nw', highlightthickness=0)
        self.params_label.grid(row=2, column=3, columnspan=2, sticky=tk.NSEW)

        self.start = tk.Button(command=self.main, text='START')
        self.start.grid(row=3, column=2)

        density_label = tk.Label(self.window, text="PARAMETERS")
        density_label.grid(row=4, column=0, columnspan=3)

        rate_label = tk.Label(self.window, text="Infection rate")
        rate_label.grid(row=5, column=0, columnspan=2)
        self.rate_label = tk.Entry(self.window)
        self.rate_label.grid(row=5, column=1, columnspan=2)

        serial_label = tk.Label(self.window, text="Serial interval")
        serial_label.grid(row=6, column=0, columnspan=2)
        self.serial_entry = tk.Entry(self.window)
        self.serial_entry.grid(row=6, column=1, columnspan=2)

        contagious_label = tk.Label(self.window, text="Contagious period")
        contagious_label.grid(row=7, column=0, columnspan=2)
        self.contagious_entry = tk.Entry(self.window)
        self.contagious_entry.grid(row=7, column=1, columnspan=2)

        fatality_label = tk.Label(self.window, text="Fatality")
        fatality_label.grid(row=8, column=0, columnspan=2)
        self.fatality_entry = tk.Entry(self.window)
        self.fatality_entry.grid(row=8, column=1, columnspan=2)

        immunity_label = tk.Label(self.window, text="Immunity")
        immunity_label.grid(row=9, column=0, columnspan=2)
        self.immunity_entry = tk.Entry(self.window)
        self.immunity_entry.grid(row=9, column=1, columnspan=2)

        quarantine_label = tk.Label(self.window, text="QUARANTINE")
        quarantine_label.grid(row=4, column=2, columnspan=3)

        q_introduced_label = tk.Label(self.window,
                                      text="Quarantine introduced")
        q_introduced_label.grid(row=5, column=2, columnspan=2)
        self.q_introduced_entry = tk.Entry(self.window)
        self.q_introduced_entry.grid(row=5, column=3, columnspan=2)

        q_effectiveness_label = tk.Label(self.window,
                                         text="Quarantine effectiveness")
        q_effectiveness_label.grid(row=6, column=2, columnspan=2)
        self.q_effectiveness_entry = tk.Entry(self.window)
        self.q_effectiveness_entry.grid(row=6, column=3, columnspan=2)

        medication_label = tk.Label(self.window, text="MEDICATION")
        medication_label.grid(row=7, column=2, columnspan=3)

        med_invented_label = tk.Label(self.window,
                                        text="Medication invented")
        med_invented_label.grid(row=8, column=2, columnspan=2)
        self.med_invented_entry = tk.Entry(self.window)
        self.med_invented_entry.grid(row=8, column=3, columnspan=2)

        med_effectiveness_label = tk.Label(self.window,
                                           text="Medication effectiveness")
        med_effectiveness_label.grid(row=9, column=2, columnspan=2)
        self.med_effectiveness_entry = tk.Entry(self.window)
        self.med_effectiveness_entry.grid(row=9, column=3, columnspan=2)

        simulation_label = tk.Label(self.window, text="SIMULATION")
        simulation_label.grid(row=10, column=2)

        filename_label = tk.Label(self.window, text="Filename")
        filename_label.grid(row=11, column=1, columnspan=2)
        self.filename_entry = tk.Entry(self.window)
        self.filename_entry.grid(row=11, column=2, columnspan=2)

        self.window.mainloop()

    def get_input(self):
        rate = self.rate_label.get()
        if rate:
            self.simulation.RATE = float(rate)
        serial = self.serial_entry.get()
        if serial:
            self.simulation.SERIAL = int(serial)
        contagious = self.contagious_entry.get()
        if contagious:
            self.simulation.CONTAGIOUS = int(contagious)
        fatality = self.fatality_entry.get()
        if fatality:
            self.simulation.FATALITY = float(fatality)
        immunity = self.immunity_entry.get()
        if immunity:
            self.simulation.IMMUNITY = float(immunity)
        q_introduced = self.q_introduced_entry.get()
        if q_introduced:
            self.simulation.Q_INTRODUCED = int(q_introduced)
        q_effectiveness = self.q_effectiveness_entry.get()
        if q_effectiveness:
            self.simulation.Q_EFFECTIVENESS = float(q_effectiveness)
        med_invented = self.med_invented_entry.get()
        if med_invented:
            self.simulation.MED_INVENTED = int(med_invented)
        med_effectiveness = self.med_effectiveness_entry.get()
        if med_effectiveness:
            self.simulation.MED_EFFECTIVENESS = float(med_effectiveness)
        filename = self.filename_entry.get()
        if filename:
            self.simulation.FILENAME = f"{filename}.csv"

    def main(self):
        self.get_input()
        self.simulation.main()


Application()
