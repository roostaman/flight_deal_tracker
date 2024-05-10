import requests
from datetime import datetime, timedelta
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = "ctfpTEALRX0jwB_WPXnEkjurENcwZ0QIc"
HEADER = {"apikey": TEQUILA_API_KEY}
MY_CITY = "NQZ"


class FlightSearch:

    def flight_search(self, city_check):
        now = datetime.now().date()
        date_from = now.strftime("%d/%m/%Y")
        days_later = now + timedelta(days=30 * 6)
        date_to = days_later.strftime("%d/%m/%Y")

        query = {
            "fly_from": f"city:{MY_CITY}",
            "fly_to": f"city:{city_check}",
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }
        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/search",
            headers=HEADER,
            params=query
        )
        try:
            data = response.json()["data"][0]
            # print(data)
        except IndexError:
            print(f"No flights found to: {city_check}")
            return None
        # print(data)
        else:
            out_date = data["route"][0]["dTime"]
            return_date = data["route"][1]["dTime"]
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=datetime.utcfromtimestamp(out_date),
                return_date=datetime.utcfromtimestamp(return_date)
            )
            # print(datetime.utcfromtimestamp(out_date))
            print(f"{flight_data.destination_city}: ${flight_data.price}")
            return flight_data

    def get_destination_code(self, city_name):
        query = {
            "term": city_name,
            "location_types": "city"
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", headers=HEADER, params=query)
        data = response.json()
        # print(data)
        city_code = data["locations"][0]["code"]
        return city_code
