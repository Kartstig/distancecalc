
import requests, json, time
from datetime import datetime

from Config import API_KEY

epoch = datetime.utcfromtimestamp(0)

TIME_H_START = 7
TIME_H_STOP = 17
TIME_INTERVAL = 1
TIME_QUERIES = [ datetime(2017, 5, 16, hour=hour) for hour in \
    range(TIME_H_START,TIME_H_STOP+TIME_INTERVAL, TIME_INTERVAL)
]
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/"
GMAPS_DIRECTIONS_URL = GMAPS_BASE_URL + "directions/json?" 

# Directions Settings
TRAVEL_MODE="DRIVING"
TRAFFIC_MODEL="best_guess"
UNITS="imperial"


def get_directions(origin, destination, departure_time=None):
    params = {
        "departure_time": round((departure_time-epoch).total_seconds()),
        "travel_mode": TRAVEL_MODE,
        "traffic_model": TRAFFIC_MODEL,
        "units": UNITS,
        "origin": origin,
        "destination": destination,
        "key": API_KEY
    }
    return requests.get(GMAPS_DIRECTIONS_URL, params=params)

def get_total_time(routes):
    total_time = 0
    for route in routes:
        for leg in route["legs"]:
            total_time += leg["duration"]["value"]

    return total_time

def main():
    origin = "2138 Triad Court Columbus OH 43235"
    destination = "41 S High St #1400, Columbus, OH 43215"

    for departure_time in TIME_QUERIES:
        response = get_directions(
            origin="+".join(origin.split()),
            destination="+".join(destination.split()),
            departure_time=departure_time
        )
        if response.ok:
            routes = response.json()["routes"]
            total_time = get_total_time(routes)
            msg = """
            Origin: {origin}
            Destination: {destination}
            Departure: {departure_time}
            Time: {total_time} minutes
            """.format(
                origin=origin,
                destination=destination,
                departure_time=departure_time.strftime("%Y/%m/%d - %H:%M"),
                total_time=total_time/60
            )
        else:
            msg = """
            Error. HTTP {code}

            Response: {body}

            """.format(
                code=response.status_code,
                body=response.text
            )
        print(msg)
        time.sleep(2)

if __name__ == '__main__':
    main()
