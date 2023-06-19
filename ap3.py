import random
import time
import math

class Wind:
    def __init__(self):
        self.direction = self.generate_direction()
        self.strength = self.generate_strength()

    def generate_direction(self):
        return random.randint(0, 360)

    def generate_strength(self):
        return random.randint(0, 12)

class Port:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

class RouteLeg:
    def __init__(self, start_port, end_port, distance, azimuth):
        self.start_port = start_port
        self.end_port = end_port
        self.distance = distance
        self.azimuth = math.radians(azimuth)

class Autopilot:
    def __init__(self):
        self.wind = Wind()
        self.route_legs = self.setup_route_legs()
        self.current_leg_index = 0
        self.distance_to_next_port = self.route_legs[0].distance
        self.next_port = self.route_legs[0].end_port
        self.heading = self.route_legs[0].azimuth

    def setup_route_legs(self):
        gdynia = Port("Gdyni", 54.521961, 18.530705)
        klajpeda = Port("Kłajpedy", 55.703729, 21.141404)
        karlskrona = Port("Karlskrony", 56.161632, 15.586611)
        swinoujscie = Port("Świnoujścia", 53.910957, 14.231071)

        route_legs = [
            RouteLeg(gdynia, klajpeda, 212.5, 51.671389),
            RouteLeg(klajpeda, karlskrona, 351, 278),
            RouteLeg(karlskrona, swinoujscie, 265, 198.869)
        ]

        return route_legs

    def calculate_rudder_angle(self):
        wind_strength = self.wind.strength

        if wind_strength <= 3:
            return 0
        elif wind_strength <= 6:
            return random.randint(-10, 10)
        else:
            return random.randint(-30, 30)

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad
        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    def update_position(self):
        delta_lat = (self.distance_to_next_port / 111.0) * math.cos(self.heading)
        delta_lon = (self.distance_to_next_port / 111.0) * math.sin(self.heading)

        self.current_leg.start_port.latitude += math.degrees(delta_lat)
        self.current_leg.start_port.longitude += math.degrees(delta_lon)

    def print_status(self):
        print(
            "Dotarłeś do", self.current_leg.start_port.name + ". Zmieniam kurs w stronę", self.current_leg.end_port.name + ".",
            "Kurs:", math.degrees(self.heading),
            "Kierunek wiatru:", self.wind.direction,
            "Siła wiatru (Beaufort):", self.wind.strength,
            "Kąt steru:", self.calculate_rudder_angle()
        )

    def navigate(self):
        while True:
            self.wind = Wind()
            self.current_leg = self.route_legs[self.current_leg_index]

            self.update_position()
            self.distance_to_next_port -= 50

            if self.distance_to_next_port <= 0:
                if self.current_leg_index > 0:
                    print("Dotarłeś do", self.current_leg.start_port.name + ". Zmieniam kurs w stronę", self.current_leg.end_port.name + ".")

                if self.current_leg_index == len(self.route_legs) - 1:
                    print("Dotarłeś do", self.current_leg.end_port.name + ". Koniec trasy.")
                    break

                self.current_leg_index += 1
                self.distance_to_next_port = self.route_legs[self.current_leg_index].distance
                self.heading = self.route_legs[self.current_leg_index].azimuth
                self.next_port = self.route_legs[self.current_leg_index].end_port

            self.print_status()

            time.sleep(3)


autopilot = Autopilot()
autopilot.navigate()
