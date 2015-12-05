import googlemaps
from datetime import datetime


class Client:
    googlemaps_cls = googlemaps.Client

    def __init__(self, api_key):
        self.client = self.googlemaps_cls(api_key)

    def travel_time_response(self, source, destination, departure_time):
        response = self.client.directions(
            origin=source, destination=destination, mode="driving",
            alternatives=False, departure_time=departure_time)
        return response[0]['legs'][0]['duration_in_traffic']


    def travel_time(self, source, destination,
                    departure_time_factory=datetime.now):
        return self.travel_time_response(
            source, destination, departure_time_factory())['value']

    def print_travel_time(self, source, destination,
                          departure_time_factory=datetime.now, print_=print):
        response = self.travel_time_response(
            source, destination, departure_time=departure_time_factory())
        print_(response['text'])


if __name__ == '__main__':
    API_KEY = ""
    WORK = ""
    HOME = ""

    client = Client(API_KEY)
    print('Home to work:')
    client.print_travel_time(HOME, WORK)
    print('Work to home:')
    client.print_travel_time(WORK, HOME)
