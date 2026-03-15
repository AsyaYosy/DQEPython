import datetime
from random import randrange


class PublishEssentian:
    def __init__(self, datatype, text):
        self.datatype = datatype
        self.text = text

    def publish_datatype(self):
        return f"{self.datatype}\n"

    def publish_something(self):
        return f"{self.text}\n"


class News(PublishEssentian):
    def __init__(self, city, datatype, text):
        super().__init__(datatype, text)
        self.city = city

    def publish_city(self):
        x = datetime.datetime.now()
        return f"{self.city}, {x.strftime('%x')} {x.strftime('%X')}\n\n"


class Private(PublishEssentian):
    def __init__(self, date, datatype, text):
        super().__init__(datatype, text)
        self.date = date

    def count_exp(self):
        now_date = datetime.datetime.now().date()
        date = datetime.datetime.strptime(self.date, "%Y-%m-%d").date()
        days_left = (date - now_date).days
        return f"Actual until {date}, Days left: {days_left}\n\n"


class Funny(PublishEssentian):
    def __init__(self, text, datatype):
        super().__init__(datatype, text)

    def random_lucky_day(self):
        day_dict = {
            1: "Sunday",
            2: "Monday",
            3: "Tuesday",
            4: "Wednesday",
            5: "Thursday",
            6: "Friday",
            7: "Saturday"
        }
        number = randrange(1, 8)
        return f"Your best day for {self.text}: {day_dict[number]}\n\n"
