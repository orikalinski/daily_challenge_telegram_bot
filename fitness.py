import telegram
import os
import json
from datetime import datetime, date, timedelta
import time


SAVED_EXERCISE_PATH = "./last_update.json"


class Fitness(object):
    def __init__(self):
        token = os.environ["BOT_TOKEN"]
        self.bot = telegram.Bot(token)
        self.channel = "@daily_fitness_challenge"
        self.month_to_exercise = {1: ("Push Ups", 1), 2: ("Squats", 1), 3: ("Planks", 5)}
        self.exercise_to_scale = {"Push Ups": "repetitions", "Squats": "repetitions", "Planks": "seconds"}

    def __calculate_new_fitness_exercise(self, last_exercise, month):
        exercise, incr_by = self.month_to_exercise[month]
        if exercise in last_exercise:
            last_exercise[exercise] += incr_by
        else:
            last_exercise[exercise] = incr_by

        return last_exercise

    def __prepare_pretty_message(self, exercises):
        pretty_message = "Let's Go!\nToday's Challenge:\n"
        for exercise, rep in exercises.items():
            scale = self.exercise_to_scale[exercise]
            pretty_message += "%s - %s %s\n" % (exercise, rep, scale)
        return pretty_message

    @staticmethod
    def __read_last_update():
        with open(SAVED_EXERCISE_PATH, "r") as f:
            data = json.load(f)
        data["last_update"] = datetime.strptime(data["last_update"], "%Y-%m-%d").date()
        return data

    @staticmethod
    def __update_new_exercise(new_exercise, new_date):
        with open(SAVED_EXERCISE_PATH, "w") as f:
            json.dump({"last_update": str(new_date), "exercise": new_exercise}, f)

    def broadcast_daily_exercise(self):
        while True:
            data = self.__read_last_update()

            last_exercise_date = data["last_update"]
            last_exercise = data["exercise"]

            if last_exercise_date == date.today():
                print("Message was already sent today: %s" % self.__prepare_pretty_message(last_exercise))
            else:
                new_exercise_date = last_exercise_date + timedelta(days=1)
                new_exercise = self.__calculate_new_fitness_exercise(last_exercise, new_exercise_date.month)
                self.bot.send_message(self.channel, self.__prepare_pretty_message(new_exercise))
                self.__update_new_exercise(new_exercise, new_exercise_date)
            time.sleep(60)


def main():
    f = Fitness()
    f.broadcast_daily_exercise()


if __name__ == '__main__':
    main()
