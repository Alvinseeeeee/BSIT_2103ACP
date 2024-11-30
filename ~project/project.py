import time
from threading import Timer, Thread


class IponKaMuna:
    def __init__(self):
        self.accounts = {}  # Stores accounts with usernames as keys
        self.current_user = None  # Tracks the currently logged-in user

    def create_account(self, username):
        if username in self.accounts:
            print("Account already exists. Please choose a different username.")
        elif len(self.accounts) >= 5:
            print("Account limit reached. Cannot create more accounts.")
        else:
            self.accounts[username] = {"balance": 0.0, "money_added_today": False}
            print(f"Account '{username}' created successfully!")

    def login(self, username):
        if username in self.accounts:
            self.current_user = username
            print(f"Logged in as '{username}'.")
        else:
            print("Account does not exist. Please create an account first.")

    def logout(self):
        if self.current_user:
            print(f"Logged out of '{self.current_user}'.")
            self.current_user = None
        else:
            print("No user is currently logged in.")

    def add_money(self, amount):
        if self.current_user:
            if amount > 0:
                self.accounts[self.current_user]["balance"] += amount
                self.accounts[self.current_user]["money_added_today"] = True
                print(f"${amount:.2f} added to your savings.")
            else:
                print("Please enter a positive amount to add.")
        else:
            print("Please log in to add money.")

    def withdraw_money(self, amount):
        if self.current_user:
            balance = self.accounts[self.current_user]["balance"]
            if amount > balance:
                print("Insufficient balance. Withdrawal denied.")
            else:
                self.accounts[self.current_user]["balance"] -= amount
                print(f"${amount:.2f} withdrawn from your savings.")
        else:
            print("Please log in to withdraw money.")

    def check_balance(self):
        if self.current_user:
            balance = self.accounts[self.current_user]["balance"]
            print(f"Your current savings balance is: ${balance:.2f}")
        else:
            print("Please log in to check balance.")

    def display_accounts(self):
        print("\nAccounts Overview:")
        if not self.accounts:
            print("No accounts have been created yet.")
        else:
            for username, account in self.accounts.items():
                print(f" - {username}: Balance = ${account['balance']:.2f}")

    def reset_daily_status(self):
        for username, account in self.accounts.items():
            if not account["money_added_today"]:
                print(f"Reminder: '{username}' has not added money to their savings today!")
            account["money_added_today"] = False  # Reset the daily status

    def daily_notification(self):
        interval = 300  # 5 minutes
        while True:
            time.sleep(interval)
            self.reset_daily_status()


def main():
    ipon_ka_muna = IponKaMuna()

    # Start daily notification thread
    notification_thread = Thread(target=ipon_ka_muna.daily_notification)
    notification_thread.daemon = True  # Ensures it exits when the main program ends
    notification_thread.start()

    while True:
        ipon_ka_muna.display_accounts()  # Display all accounts every time the menu appears
        print("\nIponKaMuna System")
        print("1. Create Account")
        print("2. Log In")
        print("3. Log Out")
        print("4. Add Money")
        print("5. Withdraw Money")
        print("6. Check Balance")
        print("7. Exit")
        choice = input("Choose an option (1-7): ")

        if choice == '1':
            username = input("Enter a username for the account: ")
            ipon_ka_muna.create_account(username)
        elif choice == '2':
            username = input("Enter your username: ")
            ipon_ka_muna.login(username)
        elif choice == '3':
            ipon_ka_muna.logout()
        elif choice == '4':
            try:
                amount = float(input("Enter amount to add: "))
                ipon_ka_muna.add_money(amount)
            except ValueError:
                print("Invalid input. Please enter a numerical value.")
        elif choice == '5':
            try:
                amount = float(input("Enter amount to withdraw: "))
                ipon_ka_muna.withdraw_money(amount)
            except ValueError:
                print("Invalid input. Please enter a numerical value.")
        elif choice == '6':
            ipon_ka_muna.check_balance()
        elif choice == '7':
            print("Exiting the Money Saving System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

