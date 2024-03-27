import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('training_database.db')
cursor = conn.cursor()

# pull the name and employee_ids from the employee_training table
query = "SELECT employee_id, name FROM employee_training"
cursor.execute(query)
query_results = cursor.fetchall()
i = 1

# Generate and insert the data
for row in query_results:
    id = i  # Example employee_id, adjust as needed
    employee_id = row[0]
    name = row[1]
    email = f"employee{i}.name@example.com"
    i += 1

    

    # Prepare the insert statement
    insert_stmt = 'INSERT INTO employees (id, employee_id, name, email) VALUES (?, ?, ?, ?)'
    
    # Execute the insert statement
    cursor.execute(insert_stmt, (id, employee_id, name, email))

# Commit and close
conn.commit()
conn.close()
