import sqlite3
DB_NAME = 'bank_accounts.db'


def initialize_database():
    connection = sqlite3.connect(DB_NAME)
    print("Connected to the database.")
    cursor = connection.cursor()
    print("Cursor created.")
    # Create a bank_accounts table to store user information
    print("Creating table if it does not exist...")
    cursor.execute('DROP TABLE IF EXISTS bank_accounts')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bank_accounts
        (account_id integer primary key, 
        name text, 
        pin integer,
        funds integer)          
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions
            (transaction_id integer primary key, 
            account_id integer, 
            amount real, 
            transaction_type text,
            FOREIGN KEY (account_id) REFERENCES bank_accounts(account_id))
    ''')
    print("Table created.")
    # Insert bank_accounts data
    print("Inserting Bank_accounts data...")
    cursor.execute('''
        INSERT INTO bank_accounts (name, pin, funds) VALUES
        ('John Doe', 5678, 2031),
        ('Jane Smith', 9101, 5000)
    ''')
    
    print("Bank_accounts data inserted.")
    # Commit the changes and close the connection
    print("Committing changes and closing the connection...")
    connection.commit()
    connection.close()


initialize_database()
