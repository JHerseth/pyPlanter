import datetime as dt
from datetime import timedelta
import logging
import random

SEED = 897354

random.seed(SEED)

logging.basicConfig(level=logging.WARNING)

# logger = logging.getLogger('pyPlanter')
# logger.setLevel(logging.DEBUG)


class Plant:
    def __init__(self, name: str, schedule: int, optimal_moisture: int, optimal_ph: float, health=100):
        """
        Defines a plant

        :param name: name of plant -> string
        :param schedule: how often it should be watered in days -> int
        :param optimal_moisture: optimal soil moisture level (0-100) -> int
        :param optimal_ph: optimal soil PH level (0-100) -> int
        :param health: plant health (0-100) -> int
        """
        self.name = name
        self.schedule = timedelta(days=schedule)
        self.optimal_moisture = optimal_moisture
        self.moisture = optimal_moisture
        self.optimal_ph = optimal_ph
        self.ph = optimal_ph
        self.watertime = dt.date.today()
        self.health = health
        self.alive = True

    def __repr__(self):
        day = "day" if self.schedule.days == 1 else "days"
        return f"Plant:\t\t\t\t{self.name}\n" \
               f"Schedule:\t\t\t{self.schedule.days} {day}\n" \
               f"Optimal moisture:\t{self.optimal_moisture}\n" \
               f"Current moisture:\t{self.moisture}\n" \
               f"Optimal PH:\t\t\t{self.optimal_ph}\n" \
               f"Current PH:\t\t\t{self.ph}\n" \
               f"Current health:\t\t{self.health}\n" \
               f"Alive:\t\t\t\t{self.alive}"

    def add_water(self, amount: int):
        self.watertime = dt.date.today()
        old_moisture = self.moisture
        self.moisture = self.moisture + amount
        logging.debug(f'Added {amount} ml water.\n'
                      f'Old amount:\t{old_moisture}\n'
                      f'New amount:\t{self.moisture}')

    def add_lime(self, amount: float):
        self.ph = round(self.ph + amount * 0.1, 1)

    def add_aluminumsulfate(self, amount: float):
        self.ph = round(self.ph - amount * 0.1, 1)

    def next_water_time(self):
        return self.watertime + self.schedule

    def take_damage(self, dmg: int):
        """
        :param dmg: amount of damage the plant takes
        :return: remaining health
        """
        self.health = self.health - dmg

    def get_health(self):
        return self.health

    def is_alive(self):
        return self.health >= 1

    def tick(self):
        self.alive = self.is_alive()
        self.moisture = self.moisture - random.uniform(1, 2)
        if (self.optimal_moisture * 0.9 > self.moisture) or (self.moisture > self.optimal_moisture * 1.1):
            self.take_damage(abs(self.optimal_moisture - self.moisture))

        self.ph = round(self.ph + self.ph * random.uniform(-0.1, 0.03), 1)


class Planter:
    def __init__(self, plants: list):
        self.plants = plants

    def add_plant(self, plant):
        self.plants.append(plant)

    def get_plants(self):
        return self.plants

    def get_plant_count(self):
        return len(self.plants)

    def has_dead_plants(self):
        for plant in self.plants:
            if not plant.alive:
                return True
        return False

    def get_dead_plants(self):
        return [plant for plant in self.plants if plant.alive is False]

    def get_live_plants(self):
        return [plant for plant in self.plants if plant.alive is True]

    def tick(self):
        for plant in self.plants:
            plant.tick()


cactus = Plant("cactus", 14, 20, 5.8)
orchid = Plant("Orchid", 7, 30, 6.0)
planter = Planter([cactus, orchid])

# print(planter.get_plants())
# print(planter.get_plant_count())
print(planter.has_dead_plants())


while not planter.has_dead_plants():
    print(cactus)
    print("-----------------")
    planter.tick()
    cactus.add_water(1)

if planter.has_dead_plants():
    print("found dead plants:")
    print(planter.get_dead_plants())

print("living:\n")
print(planter.get_live_plants())
