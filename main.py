from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from user_manager import UserManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
# print(sheet_data)
flight_search = FlightSearch()
notify = NotificationManager()
user_manager = UserManager()

user_manager.add_user()

# get IATA codes
if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(f"sheet_data:\n {sheet_data}")

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}

# search flights and if price is low, get sms
for destination_code in destinations:
    flight = flight_search.flight_search(destination_code)

    if flight is None:
        continue

    if destinations["lowestPrice"] > flight.price:
        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        message = (f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} "
                   f"to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} "
                   f"to {flight.return_date}.")

        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        notify.send_emails(emails, message)
