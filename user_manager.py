import requests

SHEETY_ENDPOINT = "https://api.sheety.co/c3f7b37f95b9f13d4455ea5c9e74548c/flightDealUsers/prices"


class UserManager:
    def add_user(self):
        global user_email
        print("Welcome to Rustam's flight club!")

        first_name = input("Your First Name?:")
        last_name = input("Your Last Name?:")

        is_email_got = False
        while not is_email_got:
            user_email = input("Your email?:")
            user_email_check = input("Type your email again:")
            if user_email != user_email_check:
                print("Please, type your email correctly.")
            elif user_email == user_email_check:
                is_email_got = True
        print("You're in the club!")
        parameters = {
            "price": {
                "firstName": first_name,
                "lastName": last_name,
                "email": user_email,
            }
        }

        response = requests.post(
            url=SHEETY_ENDPOINT,
            json=parameters
        )
        print(response.text)
