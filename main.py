import sqlite3 # Importing the database
import time 

options = ('1. Login to your bank account',
           '2. Open a new bank account')
print('Welcome to the Bank Management System')
print('Please select an option:')
for option in options:
    print(option)
DB_NAME = 'bank_accounts.db'
connection = sqlite3.connect(DB_NAME)

def main():
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1': # Selction option 1
        account_login = input("Enter your first name and last name: ")
        account_pin = input("Enter your pin: ")
        if account_login == 'Admin' and account_pin == '1234':
            print("Welcome Admin!")
            while True:
                print("\nAdmin Menu:")
                print("1. Close a bank account")
                print("2. Modify a bank account")
                print("3. Open a new bank account")
                print("4. Exit")
                admin_choice = input("Enter your choice: ")

                if admin_choice == '1':
                    print("Listing all accounts:")
                    time.sleep(1)
                    cursor = connection.cursor()
                    cursor.execute('SELECT account_id, name, funds FROM bank_accounts')
                    accounts = cursor.fetchall()
                    for account in accounts:
                        print(f"Account ID: {account[0]}, Name: {account[1]}, Balance: ${account[2]}")

                    account_id_to_close = input("Enter the account ID to close: ")
                    time.sleep(1)
                    cursor.execute('DELETE FROM bank_accounts WHERE account_id = ?', (account_id_to_close,))
                    connection.commit()
                    print(f"Account with ID {account_id_to_close} has been closed.")

                elif admin_choice == '2':
                    account_id_to_modify = input("Enter the account ID to modify: ")
                    new_name = input("Enter the new name: ")
                    new_pin = input("Enter the new PIN: ")
                    new_funds = input("Enter the new funds: ")
                    cursor = connection.cursor()
                    cursor.execute('''
                        UPDATE bank_accounts
                        SET name = ?, pin = ?, funds = ?
                        WHERE account_id = ?
                    ''', (new_name, new_pin, new_funds, account_id_to_modify))
                    connection.commit()
                    print('Updating account...')
                    time.sleep(1)
                    print(f"Account with ID {account_id_to_modify} has been updated.")

                elif admin_choice == '3':
                    print("Opening a new bank account...")
                    new_name = input("Enter the name for the new account: ")
                    new_pin = input("Enter the PIN for the new account: ")
                    new_funds = input("Enter the initial deposit amount: ")
                    cursor = connection.cursor()
                    cursor.execute('''
                        INSERT INTO bank_accounts (name, pin, funds)
                        VALUES (?, ?, ?)
                    ''', (new_name, new_pin, new_funds))
                    connection.commit()
                    time.sleep(1)  
                    print(f"Account for {new_name} has been created.")

                elif admin_choice == '4':
                    print("Exiting Admin Menu.")
                    break

                else:
                    print("Invalid choice. Please try again.")

        else:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM bank_accounts WHERE LOWER(name) = LOWER(?) AND pin = ?', (account_login.lower(), account_pin))
            user = cursor.fetchone()

            if user:
                print(f"Welcome {user[1]}!")  # user[1] is the name column
                print(f"Your current balance is: ${user[3]}")  # user[3] is the funds column
                while True:
                    print("\nUser Menu:")
                    print("1. View Balance")
                    print("2. Deposit Funds")
                    print("3. Withdraw Funds")
                    print("4. Logout")
                    user_choice = input("Enter your choice: ")

                    if user_choice == '1':
                        print(f"Your current balance is: ${user[3]}")

                    elif user_choice == '2':
                        deposit_amount = float(input("Enter the amount to deposit: "))
                        user = list(user)  # Convert tuple to list for modification
                        user[3] += deposit_amount
                        cursor.execute('UPDATE bank_accounts SET funds = ? WHERE account_id = ?', (user[3], user[0]))
                        connection.commit()
                        print(f"${deposit_amount} has been deposited. Your new balance is: ${user[3]}")

                    elif user_choice == '3':
                        withdraw_amount = float(input("Enter the amount to withdraw: "))
                        if withdraw_amount > user[3]:
                            print("Insufficient funds.")
                        else:
                            user = list(user)  
                            user[3] -= withdraw_amount
                            cursor.execute('UPDATE bank_accounts SET funds = ? WHERE account_id = ?', (user[3], user[0]))
                            connection.commit()
                            print(f"${withdraw_amount} has been withdrawn. Your new balance is: ${user[3]}")

                    elif user_choice == '4':
                        print("Successfully logged out.") 
                        break # ends the code/loop

                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid credentials. Please try again.")

    elif choice == '2':
        print("Opening a new bank account.")
        new_name = input("Enter your full name: ")
        new_pin = input("Enter a 4-digit PIN: ")
        new_funds = float(input("Enter the initial deposit amount: "))
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO bank_accounts (name, pin, funds)
            VALUES (?, ?, ?)
        ''', (new_name, new_pin, new_funds)) # adding the new account to the database
        connection.commit()
        print(f"Account for {new_name} has been successfully created!")

    else:
        print("Invalid choice. Please restart the program and try again.")

    connection.close() # closes the connection to the database


if __name__ == "__main__": # runs the code
    main()