import math
import sqlite3

class CityDistance:
    def __init__(self, city1, city2, coordinates_city_1, coordinates_city_2):
        self.city1 = city1
        self.city2 = city2
        self.coordinates_city_1 = coordinates_city_1
        self.coordinates_city_2 = coordinates_city_2

    def create_database(self):
        conn = sqlite3.connect('city_distances.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS distances (
                id INTEGER PRIMARY KEY,
                city1 TEXT,
                city2 TEXT,
                distance REAL
            )
        ''')
        conn.commit()
        conn.close()

    def add_distance(self):
        conn = sqlite3.connect('city_distances.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT distance FROM distances
            WHERE (city1 = ? AND city2 = ?) OR (city1 = ? AND city2 = ?)
        ''', (self.city1, self.city2, self.city2, self.city1))
        result = cursor.fetchone()
        if result:
            message = f"Distance between {self.city1} and {self.city2} already exists: {result[0]:.2f} km"
        else:
            self.enter_coordinates()
            distance = self.distance_km()
            cursor.execute('''
            INSERT INTO distances (city1, city2, distance) VALUES (?, ?, ?)
            ''', (self.city1, self.city2, distance))
            conn.commit()
            message = f"Distance between {self.city1} and {self.city2} saved to database: {distance:.2f} km"
        conn.close()
        return message
    
    def enter_coordinates(self):
        self.coordinates_city_1 = tuple(map(float, input(f"Enter coordinates for {self.city1} (lat lon): ").split()))
        self.coordinates_city_2 = tuple(map(float, input(f"Enter coordinates for {self.city2} (lat lon): ").split()))

    def distance_km(self):
        lat1, lon1 = map(math.radians, self.coordinates_city_1)
        lat2, lon2 = map(math.radians, self.coordinates_city_2)
        d_lat = lat2 - lat1
        d_lon = lon2 - lon1
        a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return 6371.0 * c
    


if __name__ == "__main__":
    city1 = input("Enter the name of the first city: ")
    city2 = input("Enter the name of the second city: ")

    city_distance = CityDistance(city1, city2, (0, 0), (0, 0))
    city_distance.create_database()
    print(city_distance.add_distance())