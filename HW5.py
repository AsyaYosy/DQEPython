import datetime
from random import randrange

class PublishEssentian():
    def __init__(self,datatype,text):
        self.datatype = datatype
        self.text = text

    def publish_datatype(self):
        return (f"{self.datatype}\n")
    
    def publish_something(self):
        return (f"{self.text}\n")
    
class News(PublishEssentian):
    def __init__(self,city,datatype,text):
        super().__init__(datatype,text)
        self.city = city

    def publish_city(self):
        x = datetime.datetime.now()
        return (f"{self.city},{x.strftime('%x')} {x.strftime('%X')}\n\n")


class Private(PublishEssentian):
    def __init__(self,date,datatype,text):
        super().__init__(datatype,text)
        self.datatype = datatype
    
    def count_exp(self):
        now_date = datetime.datetime.now().date()
        date = datetime.datetime.strptime(self.date, "%Y-%m-%d").date()
        days_left = abs((date - now_date).days)
        return (f"Actual until {date}, Days left: {days_left}\n\n")
    
class Funny(PublishEssentian):
    def __init__(self,text,datatype):
        super().__init__(datatype,text)

    @staticmethod
    def random_lucky_day():
        day_dict = {1:"Sunday",2:"Monday",3:"Tuesday",4:"Wensday",5:"Thursday",6:"Friday",7:"Saturday"}
        number = randrange(1,8)
        return (f"{day_dict[number]}\n\n")


class User_Interface():
    @staticmethod
    def create_new():
        print("Select type: 1 - New, 2 - Private Ad, 3 - Entertainment")
        choice = input("Your choice (1/2/3): ")
        with open("board.txt","a", encoding="utf-8") as f:
            if choice == "1":
                city = input("Enter city: ")
                text = input("Enter text: ")
                
                new = News(city,"News",text)
                f.write(new.publish_datatype())
                f.write(new.publish_something())
                f.write(new.publish_city())

            elif choice == "2":
                date = input("Enter expiration date (YYYY-MM-DD): ")
                text = input("Enter text: ")

                private_ad = Private(date,"Private Ad",text)
                f.write(private_ad.publish_datatype())
                f.write(private_ad.publish_something())
                f.write(private_ad.count_exp())

            elif choice == "3":
                text = input("Tell what are you gonna do and the universe will answer what weekday would be the luckiest for you: ")
                
                funny = Funny(text,"Entertainment")
                f.write(funny.publish_datatype())
                f.write(funny.publish_something())
                f.write(funny.random_lucky_day())

            else:
                print("Invalid choice. Please select 1 or 2 or 3.")

User_Interface.create_new()




        


            



    


