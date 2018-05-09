import datetime as dt
from datetime import timedelta
import logging
import random

SEED = 897354

random.seed(SEED)

logging.basicConfig(level=logging.DEBUG)

# logger = logging.getLogger('pyPlanter')
# logger.setLevel(logging.DEBUG)

class Plant():
    def __init__(self, name: str, schedule: int, optimal_moisture: int, optimal_ph: float, health = 100):
        '''
        :param name: Name of plant
        :param schedule: How often the plant should be watered in days
        :param optimalmoisture: Optimal moisture level for plant (0-100)
        :param health: Health of plant (0-100)
        '''
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
        self.old_moisture = self.moisture
        self.moisture = self.moisture + amount
        logging.debug(f'Added {amount} ml water.\n'
                      f'Old amount:\t{self.old_moisture}\n'
                      f'New amount:\t{self.moisture}')

    def add_lime(self, amount: float):
        self.ph = round(self.ph + amount * 0.1, 1)

    def add_aluminumsulfate(self, amount: float):
        self.ph = round(self.ph - amount * 0.1, 1)

    def next_water_time(self):
        return self.watertime + self.schedule

    def take_damage(self, dmg: int) -> int:
        '''
        :param dmg: amount of damage the plant takes
        :return: remaining health
        '''
        self.health = self.health - dmg

    def get_health(self):
        return self.health

    def is_alive(self):
        return self.health >= 1

    def tick(self):
        self.alive = self.is_alive()
        self.moisture = self.moisture - random.uniform(1,2)
        if (self.optimal_moisture * 0.9 > self.moisture) or (self.moisture > self.optimal_moisture * 1.1):
            self.take_damage(abs(self.optimal_moisture - self.moisture))

        self.ph = round(self.ph + self.ph * random.uniform(-0.1, 0.03),1)



cactus = Plant("cactus", 14, 20, 5.8)

while cactus.alive:
    print(cactus)
    print("-----------------")
    cactus.tick()
    cactus.add_water(1)
