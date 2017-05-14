
import requests, json
from datetime import datetime

from Config import API_KEY

epoch = datetime.utcfromtimestamp(0)

START = datetime(2017, 5, 15, hour=8, minute=0, second=0)

GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/"
GMAPS_DIRECTIONS_URL = GMAPS_BASE_URL + "directions/json?" 

# Directions Settings
TRAVEL_MODE="DRIVING"


def get_directions(origin, destination, departure_time=START):
    params = {
        "departure_time": round((departure_time-epoch).total_seconds()),
        "travel_mode": TRAVEL_MODE,
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

    response = get_directions(
        origin="+".join(origin.split()),
        destination="+".join(destination.split())
    )
    if response.ok:
        routes = response.json()["routes"]
        time = get_total_time(routes)
        msg = """
        Origin: {origin}
        Destination: {destination}
        Time: {time} minutes
        """.format(
            origin=origin,
            destination=destination,
            time=time/60
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

if __name__ == '__main__':
    main()
