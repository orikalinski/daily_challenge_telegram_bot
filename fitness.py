import telegram
import os
import json
from datetime import datetime, date
import time


SAVED_EXERCISE_PATH = "./last_update.json"


class Fitness(object):
    def __init__(self):
        token = os.environ["BOT_TOKEN"]
        self.bot = telegram.Bot(token)
        self.channel = "@daily_fitness_challenge"
        self.month_to_exercise = {1: "Push Ups", 2: "Squats", 3: "Pull ups"}

    def __calculate_new_fitness_exercise(self, yesterday_exercise, month):
        yesterday_exercise[self.month_to_exercise[month]] += 1
        return yesterday_exercise

    @staticmethod
    def __prepare_pretty_message(exercises):
        pretty_message = "Let's Go!\nToday's Challenge:\n"
        for exercise, rep in exercises.items():
            pretty_message += "%s %s\n" % (rep, exercise)
        return pretty_message

    @staticmethod
    def __read_last_update():
        with open(SAVED_EXERCISE_PATH, "r") as f:
            data = json.load(f)
        data["last_update"] = datetime.strptime(data["last_update"], "%Y-%m-%d").date()
        return data

    @staticmethod
    def __update_new_exercise(new_exercise):
        with open(SAVED_EXERCISE_PATH, "w") as f:
            json.dump({"last_update": str(date.today()), "exercise": new_exercise}, f)

    def broadcast_daily_exercise(self):
        while True:
            data = self.__read_last_update()

            exercise_date = data["last_update"]
            yesterday_exercise = data["exercise"]

            if exercise_date == date.today():
                print("Message was already sent today: %s" % self.__prepare_pretty_message(yesterday_exercise))
            else:
                new_exercise = self.__calculate_new_fitness_exercise(yesterday_exercise, exercise_date.month)
                self.bot.send_message(self.channel, self.__prepare_pretty_message(new_exercise))
                self.__update_new_exercise(new_exercise)
            time.sleep(60)


def main():
    f = Fitness()
    f.broadcast_daily_exercise()


if __name__ == '__main__':
    main()
