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
        self.transaction_history = []  # List to store transaction history
        self.record_transaction("Initial Deposit", initial_deposit)

    def verify_password(self, password):
        return self.password == password

    def verify_signatures(self, signatures):
        return self.signatures == signatures

    def record_transaction(self, transaction_type, amount):
        """Records a transaction with its details."""
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
        print(f"Balance: ₱{self.balance:,.2f}")
        print("\n=== Transaction History ===")
        for transaction in self.transaction_history:
            print(f"{transaction['date']} | {transaction['type']} | Amount: ₱{transaction['amount']:,.2f} | Balance: ₱{transaction['balance']:,.2f}")

    def deposit(self, amount):
        self.balance += amount
        self.record_transaction("Deposit", amount)
        print(f"Successfully added ₱{amount:,.2f}. New balance: ₱{self.balance:,.2f}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            self.record_transaction("Withdrawal", amount)
            print(f"Successfully withdrawn ₱{amount:,.2f}. Remaining balance: ₱{self.balance:,.2f}")

class BanksamoroSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self):
        print("\n=== Create a New Account ===")
        try:
            full_name = input("Enter your full name: ")
            age = int(input("Enter your age: "))
            address = input("Enter your address: ")
            initial_deposit = float(input("Enter the amount of initial deposit: "))
            if initial_deposit < 0:
                print("Initial deposit cannot be negative.")
                return
            signatures = [input(f"Enter signature {i + 1}: ") for i in range(3)]
            password = input("Set a password for your account: ")

            account = BankAccount(full_name, age, address, initial_deposit, signatures, password)
            self.accounts[full_name] = account
            print("\nAccount created successfully!")
            account.display_account_details()
        except ValueError:
            print("Invalid input. Please enter valid data.")

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
        while True:
            print("\n=== Account Menu ===")
            print("1. Add Money")
            print("2. View Account")
            print("3. Withdraw Money")
            print("4. Log Out")

            choice = input("Choose an option: ")

            if choice == "1":
                self.add_money(account)
            elif choice == "2":
                account.display_account_details()
            elif choice == "3":
                self.withdraw_money(account)
            elif choice == "4":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_money(self, account):
        print("\n=== Add Money ===")
        try:
            amount = float(input("Enter the amount to add: "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                return
            signatures = [input(f"Enter signature {i + 1}: ") for i in range(3)]

            if account.verify_signatures(signatures):
                account.deposit(amount)
            else:
                print("Invalid signatures. Transaction cancelled.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    def withdraw_money(self, account):
        print("\n=== Withdraw Money ===")
        try:
            amount = float(input("Enter the amount to withdraw: "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                return
            signatures = [input(f"Enter signature {i + 1}: ") for i in range(3)]

            if account.verify_signatures(signatures):
                account.withdraw(amount)
            else:
                print("Invalid signatures. Transaction cancelled.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

# Main Program
if __name__ == "__main__":
    bank = BanksamoroSystem()

    while True:
        print("\n=== Welcome to Banksamoro ===")
        print("1. Create a New Account")
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
