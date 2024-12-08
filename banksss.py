import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
import datetime

class BankAccount:
    def __init__(self, account_id, full_name, age, address, initial_deposit, pin):
        self.account_id = account_id
        self.full_name = full_name
        self.age = age
        self.address = address
        self.balance = initial_deposit
        self.pin = pin
        self.account_number = f"BANKSAMORO-{account_id}"
        self.transaction_history = []
        self.record_transaction("Initial Deposit", initial_deposit)

    def verify_pin(self, pin):
        return self.pin == pin

    def record_transaction(self, transaction_type, amount):
        self.transaction_history.append({
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": transaction_type,
            "amount": amount,
            "balance": self.balance
        })

    def add_money(self, amount):
        self.balance += amount
        self.record_transaction("Deposit", amount)
        messagebox.showinfo("Success", f"₱{amount:,} added to your account.\nNew Balance: ₱{self.balance:,}.")

    def withdraw(self, amount, pin):
        if not self.verify_pin(pin):
            messagebox.showerror("Error", "Invalid PIN.")
            return
        if amount > self.balance:
            messagebox.showerror("Error", "Insufficient balance.")
        else:
            self.balance -= amount
            self.record_transaction("Withdrawal", amount)
            messagebox.showinfo("Success", f"Successfully withdrawn ₱{amount:,}. Remaining balance: ₱{self.balance:,}.")

    def transfer_money(self, recipient_account, amount):
        if amount > self.balance:
            messagebox.showerror("Error", "Insufficient balance.")
        else:
            self.balance -= amount
            recipient_account.add_money(amount)
            self.record_transaction("Transfer Out", amount)
            recipient_account.record_transaction("Transfer In", amount)
            messagebox.showinfo("Success", f"Successfully transferred ₱{amount:,}.")

    def display_account_details(self):
        details = (
            f"Account Number: {self.account_number}\n"
            f"Full Name: {self.full_name}\n"
            f"Age: {self.age}\n"
            f"Address: {self.address}\n"
            f"Balance: ₱{self.balance:,}\n\n"
            "Transaction History:\n"
        )
        for t in self.transaction_history:
            details += f"{t['date']} | {t['type']} | ₱{t['amount']:,} | Balance: ₱{t['balance']:,}\n"
        messagebox.showinfo("Account Details", details)

    def play_spin_a_wheel(self):
        prizes = ["₱100", "₱500", "₱1,000", "₱5,000", "₱100,000", "Bokya"]
        chances = {
            "₱100": "50%",
            "₱500": "30%",
            "₱1,000": "10%",
            "₱5,000": "7%",
            "₱100,000": "2%",
            "Bokya": "1%"
        }

        # Show prizes and chances
        prizes_info = "\n".join([f"{prize}: Chance - {chances[prize]}" for prize in prizes])
        messagebox.showinfo("Spin A Wheel Prizes", f"Prizes and Chances:\n{prizes_info}")

        # Ask user to spin or not
        response = messagebox.askquestion("Spin A Wheel", "Do you want to spin?")
        if response == "yes":
            # 2 second delay before spin result
            time.sleep(2)
            result = random.choice(prizes)
            messagebox.showinfo("Spin A Wheel", f"Result: {result}")
            if result != "Bokya":
                amount_won = int(result.replace("₱", "").replace(",", ""))
                self.balance += amount_won
                self.record_transaction(f"Win: {result}", amount_won)
                messagebox.showinfo("Congratulations!", f"You won {result}!\nNew Balance: ₱{self.balance:,}")
        else:
            messagebox.showinfo("Spin A Wheel", "You chose not to spin.")

    def play_color_game(self):
        colors = ["black", "red", "blue", "green", "yellow", "violet"]
        color_chances = {
            "black": "20%",
            "red": "20%",
            "blue": "20%",
            "green": "20%",
            "yellow": "10%",
            "violet": "10%"
        }

        total_bet = 0
        chosen_bets = []  # List of (color, bet amount)

        while True:
            # Ask user to choose a color and place a bet
            chosen_color = simpledialog.askstring("Color Game", f"Choose a color ({', '.join(colors)}):")
            if chosen_color not in colors:
                messagebox.showerror("Error", "Invalid color. Please choose a valid color.")
                continue

            bet_amount = simpledialog.askfloat("Color Game", "Enter your bet amount:")
            if bet_amount <= 0 or bet_amount > self.balance:
                messagebox.showerror("Error", "Invalid bet amount. Ensure it is within your balance.")
                continue

            # Add the bet to the list
            chosen_bets.append((chosen_color, bet_amount))
            total_bet += bet_amount

            # Ask if the user wants to bet again
            bet_again = messagebox.askquestion("Color Game", "Do you want to bet again? (Yes/No)")
            if bet_again.lower() != "yes":
                break

        # Simulate the dice roll (randomly choosing 2 colors)
        dice_roll = random.sample(colors, 2)
        messagebox.showinfo("Color Game", f"The dice rolled: {', '.join(dice_roll)}")

        # Process the result based on the bets
        for bet in chosen_bets:
            chosen_color, bet_amount = bet
            if chosen_color in dice_roll:
                self.balance += bet_amount
                self.record_transaction(f"Win: Color Game ({chosen_color})", bet_amount)
                messagebox.showinfo("Congratulations!", f"You win {bet_amount:,} for {chosen_color}!")
            else:
                self.balance -= bet_amount
                self.record_transaction(f"Lose: Color Game ({chosen_color})", bet_amount)
                messagebox.showinfo("Better Luck Next Time", f"You lose {bet_amount:,} for {chosen_color}.")

        # Display final balance
        messagebox.showinfo("Final Balance", f"Your final balance is: ₱{self.balance:,}")

class BanksamoroSystem:
    def __init__(self, root):
        self.root = root
        self.accounts = {}
        self.current_account = None
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        self.root.title("Banksamoro System")
        self.root.geometry("600x500")
        tk.Label(self.root, text="Banksamoro System", font=("Arial", 28, "bold")).pack(pady=20)
        tk.Button(self.root, text="Create Account", command=self.create_account_window, font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Log In", command=self.login_window, font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, font=("Arial", 14)).pack(pady=10)

    def create_account_window(self):
        self.clear_window()
        tk.Label(self.root, text="Create Account", font=("Arial", 22, "bold")).pack(pady=10)
        entries = {}
        labels = ["Account ID", "Full Name", "Age", "Address", "Initial Deposit", "PIN"]

        for label in labels:
            frame = tk.Frame(self.root)
            frame.pack(pady=5)
            tk.Label(frame, text=f"{label}:", font=("Arial", 14)).pack(side=tk.LEFT)
            entry = tk.Entry(frame, show="*" if label == "PIN" else None, font=("Arial", 14))
            entry.pack(side=tk.RIGHT)
            entries[label] = entry

        def submit():
            account_id = entries["Account ID"].get()
            full_name = entries["Full Name"].get()
            age = entries["Age"].get()
            address = entries["Address"].get()
            initial_deposit = float(entries["Initial Deposit"].get())
            pin = entries["PIN"].get()

            if account_id and full_name and address and pin:
                account = BankAccount(account_id, full_name, int(age), address, initial_deposit, pin)
                self.accounts[account_id] = account
                messagebox.showinfo("Success", "Account created!")
                self.create_main_menu()

        tk.Button(self.root, text="Submit", command=submit, font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu, font=("Arial", 14)).pack(pady=5)

    def login_window(self):
        self.clear_window()
        tk.Label(self.root, text="Log In", font=("Arial", 22, "bold")).pack(pady=10)
        tk.Label(self.root, text="Account ID:", font=("Arial", 14)).pack()
        account_id_entry = tk.Entry(self.root, font=("Arial", 14))
        account_id_entry.pack()
        tk.Label(self.root, text="PIN:", font=("Arial", 14)).pack()
        pin_entry = tk.Entry(self.root, font=("Arial", 14), show="*")
        pin_entry.pack()

        def login():
            account_id = account_id_entry.get()
            pin = pin_entry.get()
            if account_id in self.accounts:
                account = self.accounts[account_id]
                if account.verify_pin(pin):
                    self.current_account = account
                    self.account_menu(account)
                else:
                    messagebox.showerror("Error", "Invalid PIN")
            else:
                messagebox.showerror("Error", "Account not found")

        tk.Button(self.root, text="Log In", command=login, font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu, font=("Arial", 14)).pack()

    def account_menu(self, account):
        self.clear_window()
        tk.Label(self.root, text=f"Welcome {account.full_name}", font=("Arial", 22, "bold")).pack(pady=10)
        tk.Button(self.root, text="View Details", command=account.display_account_details, font=("Arial", 14)).pack(pady=5)
        tk.Button(self.root, text="Play Spin A Wheel", command=account.play_spin_a_wheel, font=("Arial", 14)).pack(pady=5)
        tk.Button(self.root, text="Play Color Game", command=account.play_color_game, font=("Arial", 14)).pack(pady=5)

        # Add money, withdraw, transfer buttons
        tk.Button(self.root, text="Add Money", command=self.add_money_window, font=("Arial", 14)).pack(pady=5)
        tk.Button(self.root, text="Withdraw Money", command=self.withdraw_money_window, font=("Arial", 14)).pack(pady=5)
        tk.Button(self.root, text="Transfer Money", command=self.transfer_money_window, font=("Arial", 14)).pack(pady=5)

        tk.Button(self.root, text="Log Out", command=self.create_main_menu, font=("Arial", 14)).pack(pady=10)

    def add_money_window(self):
        amount = simpledialog.askfloat("Add Money", "Enter amount to add:", minvalue=1)
        if amount:
            self.current_account.add_money(amount)

    def withdraw_money_window(self):
        pin = simpledialog.askstring("Withdraw Money", "Enter your PIN:")
        amount = simpledialog.askfloat("Withdraw Money", "Enter amount to withdraw:", minvalue=1)
        if amount and pin:
            self.current_account.withdraw(amount, pin)

    def transfer_money_window(self):
        recipient_account_id = simpledialog.askstring("Transfer Money", "Enter recipient account ID:")
        recipient_account = self.accounts.get(recipient_account_id)
        if recipient_account:
            amount = simpledialog.askfloat("Transfer Money", "Enter amount to transfer:", minvalue=1)
            if amount:
                self.current_account.transfer_money(recipient_account, amount)
        else:
            messagebox.showerror("Error", "Recipient account not found")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BanksamoroSystem(root)
    root.mainloop()
