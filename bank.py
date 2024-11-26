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
        print(f"Balance: {self.balance}")
        print("\n=== Transaction History ===")
        for transaction in self.transaction_history:
            print(f"{transaction['date']} | {transaction['type']} | Amount: {transaction['amount']} | Balance: {transaction['balance']}")

    def deposit(self, amount):
        self.balance += amount
        self.record_transaction("Deposit", amount)
        print(f"Successfully added {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            self.record_transaction("Withdrawal", amount)
            print(f"Successfully withdrawn {amount}. Remaining balance: {self.balance}")

class BanksamoroSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self):
        print("\n=== Create a New Account ===")
        full_name = input("Enter your full name: ")
        age = int(input("Enter your age: "))
        address = input("Enter your address: ")
        initial_deposit = float(input("Enter the amount of initial deposit: "))
        signatures = [input(f"Enter signature {i + 1}: ") for i in range(3)]
        password = input("Set a password for your account: ")

        account = BankAccount(full_name, age, address, initial_deposit, signatures, password)
        self.accounts[full_name] = account
        print("\nAccount created successfully!")
        account.display_account_details()

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
            print("3. Check Out Money")
            print("4. Log Out")

            choice = input("Choose an option: ")

            if choice == "1":
                self.add_money(account)
            elif choice == "2":
                account.display_account_details()
            elif choice == "3":
                self.check_out_money(account)
            elif choice == "4":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_money(self, account):
        print("\n=== Add Money ===")
        amount = float(input("Enter the amount to add: "))
        signatures = [input(f"Enter signature {i + 1}: ") for i in range(3)]

        if account.verify_signatures(signatures):
            account.deposit(amount)
        else:
            print("Invalid signatures. Transaction cancelled.")

    def check_out_money(self, account):
        print("\n=== Check Out Money ===")
        amount = float(input("Enter the amount to withdraw: "))
        signatures = [input(f"Enter signature {i + 1}: ") for i in range(3)]

        if account.verify_signatures(signatures):
            account.withdraw(amount)
        else:
            print("Invalid signatures. Transaction cancelled.")

# Main Program
if __name__ == "__main__":
    bank = BanksamoroSystem()

    while True:
        print("\n=== Welcome to Banksamoro ===")
        print("1. Create Account for Newbie")
        print("2. Log In for Old User")
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
