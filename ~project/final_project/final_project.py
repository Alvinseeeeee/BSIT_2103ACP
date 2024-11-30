import random
import time
import datetime

class BankAccount:
    def __init__(self, full_name, age, address, initial_deposit, signatures, password):
        self.full_name = full_name
        self.age = age
        self.address = address
        self.balance = initial_deposit
        self.signatures = signatures
        self.password = password
        self.account_number = f"BANKSAMORO-{id(self)}"
        self.transaction_history = []
        self.record_transaction("Initial Deposit", initial_deposit)

    def verify_password(self, password):
        return self.password == password

    def verify_signatures(self, signatures):
        return self.signatures == signatures

    def record_transaction(self, transaction_type, amount):
        self.transaction_history.append({
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": transaction_type,
            "amount": amount,
            "balance": self.balance
        })

    def display_account_details(self):
        print("\n=== Account Details ===")
        print(f"Account Number: {self.account_number}")
        print(f"Full Name: {self.full_name}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")
        print(f"Balance: ₱{self.balance:,}")
        print("\n=== Transaction History ===")
        for transaction in self.transaction_history:
            print(f"{transaction['date']} | {transaction['type']} | Amount: ₱{transaction['amount']:,} | Balance: ₱{transaction['balance']:,}")

    def deposit(self, amount):
        self.balance += amount
        self.record_transaction("Deposit", amount)
        print(f"Successfully added ₱{amount:,}. New balance: ₱{self.balance:,}.")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            self.record_transaction("Withdrawal", amount)
            print(f"Successfully withdrawn ₱{amount:,}. Remaining balance: ₱{self.balance:,}.")

    def play_color_game(self):
        colors = ["Red", "Blue", "Green", "Orange", "Violet", "Yellow", "Black"]
        print("\n--- Welcome to the Color Game ---")
        print(f"Available colors: {', '.join(colors)}")
        print(f"Current Balance: ₱{self.balance:,}")

        bets = []

        while True:
            print("\n--- Place a Bet ---")
            try:
                bet_amount = float(input("Enter your bet amount: ₱"))
                if bet_amount > self.balance or bet_amount <= 0:
                    print("Invalid bet amount. Please check your balance and try again.")
                    continue

                chosen_color = input("Choose your color: ").capitalize()
                if chosen_color not in colors:
                    print("Invalid color choice. Please select from the available options.")
                    continue

                self.balance -= bet_amount
                bets.append((chosen_color, bet_amount))
                print(f"You bet ₱{bet_amount:,} on {chosen_color}.")

                next_action = input("Another bet? (yes to bet, roll to roll): ").lower()
                if next_action == "roll":
                    break
            except ValueError:
                print("Please enter a valid numeric value.")

        print("\nRolling the dice in 5 seconds...")
        time.sleep(5)
        dice1 = random.choice(colors)
        dice2 = random.choice(colors)
        print(f"Dice Results: {dice1} and {dice2}")

        total_winnings = 0
        for color, amount in bets:
            matches = sum([1 for dice in (dice1, dice2) if dice == color])
            if matches == 1:
                winnings = amount * 2
                print(f"🎉 Bet on {color}: 1 match! You won ₱{winnings:,}!")
            elif matches == 2:
                winnings = amount * 5
                print(f"🎉 Bet on {color}: 2 matches! You won ₱{winnings:,}!")
            else:
                winnings = 0
                print(f"😞 Bet on {color}: No matches. Better luck next time!")

            total_winnings += winnings

        self.balance += total_winnings
        print(f"Total Winnings: ₱{total_winnings:,}")
        print(f"Your new balance is: ₱{self.balance:,}")

        self.record_transaction("Color Game Winnings", total_winnings)


class SpinAWheel:
    def __init__(self):
        self.prizes = [
            ("₱1,000", 15),       # 15% chance
            ("₱4,000", 10),       # 10% chance
            ("₱500", 5),          # 5% chance
            ("₱100", 5),          # 5% chance
            ("₱10,000", 2),       # 2% chance
            ("₱50,000", 2),       # 2% chance
            ("₱1,000,000", 1),    # 1% chance
            ("Bokya", 30),        # 30% chance (no win)
            ("Bokya", 30)         # 30% chance (no win)
        ]
    
    def spin(self):
        weighted_prizes = [prize[0] for prize in self.prizes for _ in range(prize[1])]
        result = random.choice(weighted_prizes)
        
        print("Spinning the wheel...")
        time.sleep(5)

        if result == "Bokya":
            print("Bokya Sayang ahahaha!")
        else:
            print(f"Congratulations! You won {result}!")

        return result

    def play_game(self, account):
        bet_amount = 1000  # Fixed bet amount
        print(f"Your bet is fixed to ₱{bet_amount}. Let's spin the wheel!")

        result = self.spin()
        
        if result != "Bokya":
            account.balance += bet_amount  # Add the bet back to balance if they win
            account.record_transaction("Spin a Wheel Winnings", bet_amount)

        play_again = input("Do you want to spin again? (yes/no): ").strip().lower()
        if play_again == "yes":
            self.play_game(account)
        else:
            print("Thanks for playing! Come again soon.")


class BanksamoroSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self):
        print("\n=== Create a New Account ===")
        full_name = input("Enter your full name: ")
        try:
            age = int(input("Enter your age: "))
            address = input("Enter your address: ")
            initial_deposit = float(input("Enter the amount of initial deposit: "))
            signatures = [input(f"Enter signature {i + 1}: ") for i in range(3)]
            password = input("Set a password for your account: ")

            account = BankAccount(full_name, age, address, initial_deposit, signatures, password)
            self.accounts[full_name] = account
            print("\nAccount created successfully!")
            account.display_account_details()
        except ValueError:
            print("Invalid input. Please try again.")

    def login(self):
        print("\n=== Log In ===")
        full_name = input("Enter your full name: ")

        if full_name in self.accounts:
            account = self.accounts[full_name]
            password = input("Enter your password: ")

            if account.verify_password(password):
                print(f"\nWelcome back, {full_name}!")
                self.account_menu(account)
            else:
                print("Invalid password.")
        else:
            print("Account not found.")

    def account_menu(self, account):
        wheel_game = SpinAWheel()  # Initialize SpinAWheel game

        while True:
            print("\n=== Account Menu ===")
            print("1. Add Money")
            print("2. View Account")
            print("3. Withdraw Money")
            print("4. Play Color Game")
            print("5. Play Spin a Wheel Game")
            print("6. Log Out")

            choice = input("Choose an option: ")

            if choice == "1":
                self.add_money(account)
            elif choice == "2":
                account.display_account_details()
            elif choice == "3":
                self.withdraw_money(account)
            elif choice == "4":
                account.play_color_game()
            elif choice == "5":
                wheel_game.play_game(account)  # Play Spin a Wheel game
            elif choice == "6":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_money(self, account):
        print("\n=== Add Money ===")
        try:
            amount = float(input("Enter the amount to add: "))
            signatures = [input(f"Enter signature {i + 1}: ") for i in range(3)]

            if account.verify_signatures(signatures):
                account.deposit(amount)
            else:
                print("Invalid signatures. Transaction cancelled.")
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

    def withdraw_money(self, account):
        print("\n=== Withdraw Money ===")
        try:
            amount = float(input("Enter the amount to withdraw: "))
            signatures = [input(f"Enter signature {i + 1}: ") for i in range(3)]

            if account.verify_signatures(signatures):
                account.withdraw(amount)
            else:
                print("Invalid signatures. Transaction cancelled.")
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")


# Main Program
if __name__ == "__main__":
    bank = BanksamoroSystem()

    while True:
        print("\n=== Welcome to Banksamoro ===")
        print("1. Create Bank Account")
        print("2. Log In")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            bank.create_account()
        elif choice == "2":
            bank.login()
        elif choice == "3":
            print("Thank you for using Banksamoro! Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
