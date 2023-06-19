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
        self.azimuth = azimuth

class Autopilot:
    def __init__(self):
        self.wind = Wind()
        self.ports = self.setup_ports()
        self.route_legs = self.setup_route_legs()
        self.current_leg_index = 0
        self.distance_to_next_port = self.route_legs[0].distance
        self.next_port = self.route_legs[0].end_port
        self.heading = self.route_legs[0].azimuth

    def setup_ports(self):
        ports = []
        port_count = int(input("Podaj liczbę portów: "))

        for i in range(port_count):
            name = input("Nazwa portu {}: ".format(i + 1))
            latitude = float(input("Szerokość geograficzna portu {}: ".format(i + 1)))
            longitude = float(input("Długość geograficzna portu {}: ".format(i + 1)))
            port = Port(name, latitude, longitude)
            ports.append(port)

        return ports

    def setup_route_legs(self):
        route_legs = []

        for i in range(len(self.ports) - 1):
            start_port = self.ports[i]
            end_port = self.ports[i + 1]
            distance = self.calculate_distance(start_port.latitude, start_port.longitude, end_port.latitude, end_port.longitude)
            azimuth = self.calculate_azimuth(start_port.latitude, start_port.longitude, end_port.latitude, end_port.longitude)
            route_leg = RouteLeg(start_port, end_port, distance, azimuth)
            route_legs.append(route_leg)

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
    
    def calculate_azimuth(self, lat1, lon1, lat2, lon2):
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        delta_lon = lon2_rad - lon1_rad
        y = math.sin(delta_lon) * math.cos(lat2_rad)
        x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)
        azimuth_rad = math.atan2(y, x)
        azimuth_deg = math.degrees(azimuth_rad)
        return azimuth_deg

    def calculate_time(self, distance, speed):
        return distance / speed

    def update_position(self):
        delta_lat = (self.distance_to_next_port / 111.0) * math.cos(math.radians(self.heading))
        delta_lon = (self.distance_to_next_port / 111.0) * math.sin(math.radians(self.heading))

        self.route_legs[self.current_leg_index].start_port.latitude += math.degrees(delta_lat)
        self.route_legs[self.current_leg_index].start_port.longitude += math.degrees(delta_lon)

    def print_status(self):
        print(
            "Dotarłeś do", self.route_legs[self.current_leg_index].start_port.name + ". Zmieniam kurs w stronę", self.route_legs[self.current_leg_index].end_port.name + ".",
            "Kurs:", self.heading,
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

                time_to_next_port = self.calculate_time(self.distance_to_next_port, 10)  
                print("Czas do następnego portu:", round(time_to_next_port, 2), "godz.")

            self.print_status()

            time.sleep(3)


autopilot = Autopilot()
autopilot.navigate()
