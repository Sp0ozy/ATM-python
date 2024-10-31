import json
import getpass
from datetime import datetime

class ATM:
    def __init__(self, data_file="data.json"):
        self.data_file = data_file
        self.user_data = self.load_user_data()
        self.current_user = None
        self.transaction_history = []

    def load_user_data(self):
        try:
            with open(self.data_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, create an empty dictionary
            return {}

    def save_user_data(self):
        with open(self.data_file, "w") as file:
            json.dump(self.user_data, file, indent=4)

    def authenticate_user(self):
        user_id = input("Enter your User ID: ")
        pin = getpass.getpass("Enter your PIN: ")

        if user_id in self.user_data and self.user_data[user_id]["pin"] == pin:
            self.current_user = user_id
            print("Authentication successful!")
            return True
        else:
            print("Incorrect User ID or PIN. Please try again.")
            return False

    def display_menu(self):
        print("\nMain Menu:")
        print("1. Withdraw")
        print("2. Deposit")
        print("3. Check Balance")
        print("4. Exit")

    def get_balance(self):
        return self.user_data[self.current_user]["balance"]

    def set_balance(self, new_balance):
        self.user_data[self.current_user]["balance"] = new_balance
        self.save_user_data()  # Save updated balance to the file

    def withdraw(self):
        amount = float(input("Enter amount to withdraw: "))
        if amount <= self.get_balance():
            new_balance = self.get_balance() - amount
            self.set_balance(new_balance)
            self.transaction_history.append(
                f"Withdrew ${amount:.2f} on {datetime.now()}"
            )
            print(f"${amount:.2f} withdrawn successfully.")
        else:
            print("Insufficient balance.")

    def deposit(self):
        amount = float(input("Enter amount to deposit: "))
        new_balance = self.get_balance() + amount
        self.set_balance(new_balance)
        self.transaction_history.append(
            f"Deposited ${amount:.2f} on {datetime.now()}"
        )
        print(f"${amount:.2f} deposited successfully.")

    def check_balance(self):
        print(f"Current balance: ${self.get_balance():.2f}")

    def display_transaction_summary(self):
        print("\nTransaction Summary:")
        if not self.transaction_history:
            print("No transactions found.")
        else:
            for transaction in self.transaction_history:
                print(transaction)

    def start(self):
        if not self.authenticate_user():
            return

        while True:
            self.display_menu()
            choice = input("Choose an option: ")

            if choice == "1":
                self.withdraw()
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.check_balance()
            elif choice == "4":
                self.display_transaction_summary()
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

# Sample JSON structure in 'user_data.json'
# {
#     "user1": {
#         "pin": "1234",
#         "balance": 1000.0
#     },
#     "user2": {
#         "pin": "5678",
#         "balance": 500.0
#     }
# }

# Create an instance of ATM and start it
atm = ATM()
atm.start()
