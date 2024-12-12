import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import time
import datetime
import os
import csv

class BankAccount:
    def __init__(self, account_id, full_name, age, address, contact_number, initial_deposit, signatures, password, user_number):
        self.account_id = account_id
        self.full_name = full_name
        self.age = age
        self.address = address
        self.contact_number = contact_number 
        self.balance = initial_deposit
        self.signatures = signatures
        self.password = password
        self.user_number = user_number
        self.account_number = f"BANKSAMORO-{account_id}"
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

    def deposit(self, amount):
        self.balance += amount
        self.record_transaction("Deposit", amount)

    def withdraw(self, amount):
        if amount > self.balance:
            messagebox.showerror("Error", "Insufficient balance.")
        else:
            self.balance -= amount
            self.record_transaction("Withdrawal", amount)
            messagebox.showinfo("Success", f"Successfully withdrawn ₱{amount:,}. Remaining balance: ₱{self.balance:,}.")

    def display_account_details(self):
        details = (
            f"Account Number: {self.account_number}\n"
            f"User Number: {self.user_number}\n"
            f"Full Name: {self.full_name}\n"
            f"Age: {self.age}\n"
            f"Address: {self.address}\n"
            f"Contact Number: {self.contact_number}\n"
            f"Balance: ₱{self.balance:,}\n\n"
            "Transaction History:\n"
        )
        for t in self.transaction_history:
            details += f"{t['date']} | {t['type']} | ₱{t['amount']:,} | Balance: ₱{t['balance']:,}\n"
        messagebox.showinfo("Account Details", details)

class BanksamoroSystem:
    def __init__(self, root):
        self.root = root
        self.accounts = {}
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        self.root.title("Banksamoro System")
        self.root.geometry("650x500")  

        tk.Label(self.root, text="Welcome to Banksamoro", font=("Arial", 28, "bold")).pack(pady=30)

        button_font = ("Arial", 16)
        tk.Button(self.root, text="Create Bank Account", font=button_font, command=self.create_account_window, width=25).pack(pady=15)
        tk.Button(self.root, text="Log In", font=button_font, command=self.login_window, width=25).pack(pady=15)
        tk.Button(self.root, text="View All Accounts", font=button_font, command=self.view_all_accounts, width=25).pack(pady=15)
        tk.Button(self.root, text="Exit", font=button_font, command=self.root.quit, width=25).pack(pady=15)

    def create_account_window(self):
        self.clear_window()
        self.root.title("Create Account")
        self.root.geometry("650x600") 

        tk.Label(self.root, text="Create a New Account", font=("Arial", 22, "bold")).pack(pady=20)

        entries = {}
        labels = ["ID", "Full Name", "Age", "Address", "Contact Number", "Initial Deposit", "Password", "User Number"]
        for label in labels:
            frame = tk.Frame(self.root)
            frame.pack(pady=10)
            tk.Label(frame, text=label + ": ", font=("Arial", 14)).pack(side=tk.LEFT)
            entry = tk.Entry(frame, show="*" if label == "Password" else None, font=("Arial", 14))
            entry.pack(side=tk.RIGHT, padx=10)
            entries[label] = entry

        def submit():
            try:
                account_id = entries["ID"].get()
                full_name = entries["Full Name"].get()
                age = int(entries["Age"].get())
                address = entries["Address"].get()
                contact_number = entries["Contact Number"].get()  
                initial_deposit = float(entries["Initial Deposit"].get())
                password = entries["Password"].get()
                user_number = entries["User Number"].get() 
                signatures = ["Signature1", "Signature2", "Signature3"]

                if account_id and full_name and address and password and user_number and contact_number:
                    account = BankAccount(account_id, full_name, age, address, contact_number, initial_deposit, signatures, password, user_number)
                    self.accounts[full_name] = account
                    messagebox.showinfo("Success", "Account created successfully!")
                    self.create_main_menu()
                else:
                    messagebox.showerror("Error", "All fields are required.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please try again.")

        tk.Button(self.root, text="Create Account", font=("Arial", 16), command=submit).pack(pady=20)
        tk.Button(self.root, text="Back", font=("Arial", 16), command=self.create_main_menu).pack(pady=5)

    def login_window(self):
        self.clear_window()
        self.root.title("Log In")
        self.root.geometry("650x500")  

        tk.Label(self.root, text="Log In", font=("Arial", 22, "bold")).pack(pady=20)

        tk.Label(self.root, text="Full Name:", font=("Arial", 14)).pack(pady=5)
        full_name_entry = tk.Entry(self.root, font=("Arial", 14))
        full_name_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=("Arial", 14)).pack(pady=5)
        password_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
        password_entry.pack(pady=5)

        def login():
            full_name = full_name_entry.get()
            password = password_entry.get()
            account = self.accounts.get(full_name)

            if account and account.verify_password(password):
                messagebox.showinfo("Success", f"Welcome back, {full_name}!")
                self.account_menu(account)
            else:
                messagebox.showerror("Error", "Invalid credentials.")

        tk.Button(self.root, text="Log In", font=("Arial", 16), command=login).pack(pady=20)
        tk.Button(self.root, text="Back", font=("Arial", 16), command=self.create_main_menu).pack(pady=5)

    def view_all_accounts(self):
        if not self.accounts:
            messagebox.showinfo("No Accounts", "No accounts have been created yet.")
            return

        account_info = "Registered Accounts:\n\n"
        for account in self.accounts.values():
            account_info += (
                f"Account Number: {account.account_number}\n"
                f"User Number: {account.user_number}\n"  
                f"Full Name: {account.full_name}\n"
                f"Age: {account.age}\n"
                f"Address: {account.address}\n"
                f"Contact Number: {account.contact_number}\n\n"  
            )

        messagebox.showinfo("All Accounts", account_info)

    def account_menu(self, account):
        self.clear_window()
        self.root.title("Account Menu")
        self.root.geometry("650x500") 

        tk.Label(self.root, text=f"Welcome, {account.full_name}", font=("Arial", 22, "bold")).pack(pady=20)

        button_font = ("Arial", 16)
        tk.Button(self.root, text="View Account Details", font=button_font, command=account.display_account_details).pack(pady=10)
        tk.Button(self.root, text="Deposit Money", font=button_font, command=lambda: self.deposit_window(account)).pack(pady=10)
        tk.Button(self.root, text="Withdraw Money", font=button_font, command=lambda: self.withdraw_window(account)).pack(pady=10)
        tk.Button(self.root, text="Log Out", font=button_font, command=self.create_main_menu).pack(pady=10)

    def deposit_window(self, account):
        amount = simpledialog.askfloat("Deposit", "Enter the amount to deposit:")
        if amount and amount > 0:
            account.deposit(amount)
            messagebox.showinfo("Success", f"Successfully deposited ₱{amount:,}.")

    def withdraw_window(self, account):
        amount = simpledialog.askfloat("Withdraw", "Enter the amount to withdraw:")
        if amount and amount > 0:
            account.withdraw(amount)

    def export_to_csv(self):
        if not self.accounts:
            messagebox.showinfo("No Accounts", "No accounts to export.")
            return

        filename = "banksamoro_accounts.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account ID", "Account Number", "Full Name", "Age", "Address", "Contact Number", "Balance", "User Number"])

            for account in self.accounts.values():
                writer.writerow([
                    account.account_id,
                    account.account_number,
                    account.full_name,
                    account.age,
                    account.address,
                    account.contact_number,  
                    f"₱{account.balance:,}",
                    account.user_number
                ])

        messagebox.showinfo("Export Successful", f"Accounts exported to '{filename}' successfully.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("650x500")  
    app = BanksamoroSystem(root)
    root.mainloop()
