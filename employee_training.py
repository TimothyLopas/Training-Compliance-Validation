import sqlite3
from random import random, randint
from datetime import date, timedelta

# Connect to your SQLite database
conn = sqlite3.connect('training_database.db')
cursor = conn.cursor()

# Ensure you've created the table in SQLite before running this script

# Function to optionally generate a future date based on probability
def generate_date(start_date, end_date, probability):
    if random() < probability:
        delta = end_date - start_date
        random_days = randint(0, delta.days)
        return start_date + timedelta(days=random_days)
    else:
        return None

# Generate and insert the data
for i in range(50):
    id = i + 1  # Example id, adjust as needed
    employee_id = i + 1  # Example employee_id, adjust as needed
    name = f'Employee Name {employee_id}'
    cybersecurity_date = generate_date(date.today(), date(2024, 4, 30), 0.8)
    anti_bribery_date = generate_date(date.today(), date(2024, 5, 30), 0.7)
    diversity_date = generate_date(date.today(), date(2024, 8, 1), 0.5)
    insider_trading_date = generate_date(date.today(), date(2024, 8, 1), 0.5)

    # Prepare the insert statement
    insert_stmt = 'INSERT INTO employee_training (id, employee_id, name, Cybersecurity_Awareness, Anti_Bribery, Diversity_Awareness, Insider_Trading_Awareness) VALUES (?, ?, ?, ?, ?, ?, ?)'
    
    # Execute the insert statement
    cursor.execute(insert_stmt, (id, employee_id, name, cybersecurity_date, anti_bribery_date, diversity_date, insider_trading_date))

# Commit and close
conn.commit()
conn.close()
