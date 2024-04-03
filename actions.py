"""
A simple AI Action template for comparing timezones

Please checkout the base guidance on AI Actions in our main repository readme:
https://github.com/robocorp/robocorp/blob/master/README.md

"""

from robocorp.actions import action
import sqlite3
from datetime import datetime

@action
def get_training_list_from_trainigns_table() -> str:
    """
    Returns a list of trainings and their associated due dates.

    Args:
        None

    Returns:
        str:  A string that contains the training name and it's due date
    """
    # Define the path to your SQLite database
    database_path = 'training_database.db'

    # Create a connection to the database
    conn = sqlite3.connect(database_path)

    # Create a cursor object using the connection
    cursor = conn.cursor()

    # SQL query to select name and due_date from the trainings table
    query = "SELECT name, due_date FROM trainings"

    tables_list = "The trainings that the company needs to complete are:\n"

    try:
        # Execute the query
        cursor.execute(query)
        
        # Fetch all rows of the query result
        rows = cursor.fetchall()
        
        # Iterate through the rows to print each record
        for row in rows:
            print(f"Name: {row[0]}, Due Date: {row[1]}")
            tables_list += f"Training Name: {row[0]}, Due Date: {row[1]}\n"
    finally:
        # Close the cursor and connection to clean up
        cursor.close()
        conn.close()
        return tables_list

    
@action
def get_completion_percentage(training_name: str) -> float:
    """
    Returns the percentage of the employees in the company who have completed the named training by the due date.

    Args:
        training_name: name of the training you want to see the percentage completion for

    Returns:
        float:  The percentage of employees who have completed the training by the due date
    """
    # Define the path to your SQLite database
    database_path = 'training_database.db'

    # Create a connection to the database
    conn = sqlite3.connect(database_path)

    # Create a cursor object using the connection
    cursor = conn.cursor()

    # SQL query to select name and due_date from the trainings table
    query_training_due_date = f"SELECT due_date FROM trainings WHERE name='{training_name}'"
    
    

    try:
        # Execute the query
        cursor.execute(query_training_due_date)
        
        # Fetch all rows of the query result
        # This will result in a list of tuples
        training_due_date_list = cursor.fetchall()
        training_due_date = training_due_date_list[0][0]
    except Exception as error:
        print(f"Query for Training Date failed: {error}")
        return 500.0

    def replace_spaces_with_underscores(input_string):
        return input_string.replace(" ", "_")

    # Since the Training name the user will input will have spaces it needs to have those spaces replaced with underscores so that the column titles match
    modified_string = replace_spaces_with_underscores(training_name)
    print(modified_string)

    # SQL query to select the number of non-null dates and dates that are less then the due date
    query_employees_who_completed_training = f"SELECT COUNT(*) AS count FROM employee_training WHERE {modified_string} IS NOT NULL AND {modified_string} < '{training_due_date}'"

    # SQL query to select the total number of employees
    query_employee_count = "SELECT COUNT(*) AS count FROM employee_training"

    try:
        cursor.execute(query_employees_who_completed_training)
        
        # Fetch all rows of the query result
        # This will result in a list of tuples
        employee_completion = cursor.fetchall()

        cursor.execute(query_employee_count)

        # Fetch all rows of the query result
        # This will result in a list of tuples
        employee_count = cursor.fetchall()
    finally:
        # Close the cursor and connection to clean up
        cursor.close()
        conn.close()
    
    try:
        employee_percentage = (employee_completion[0][0] / employee_count[0][0]) * 100
    except ZeroDivisionError:
        return 400.0
    
    return employee_percentage


@action
def get_non_completion_percentage(training_name: str) -> float:
    """
    Returns the percentage of the employees in the company who have not completed the named training by the due date.

    Args:
        training_name: name of the training you want to see the percentage completion for

    Returns:
        float:  The percentage of employees who have not completed the training by the due date
    """
    # Define the path to your SQLite database
    database_path = 'training_database.db'

    # Create a connection to the database
    conn = sqlite3.connect(database_path)

    # Create a cursor object using the connection
    cursor = conn.cursor()

    # SQL query to select name and due_date from the trainings table
    # query_training_due_date = f"SELECT due_date FROM trainings WHERE name='{training_name}'"
    
    

    # try:
    #     # Execute the query
    #     cursor.execute(query_training_due_date)
        
    #     # Fetch all rows of the query result
    #     # This will result in a list of tuples
    #     training_due_date_list = cursor.fetchall()
    #     training_due_date = training_due_date_list[0][0]
    # except Exception as error:
    #     print(f"Query for Training Date failed: {error}")
    #     return 500.0

    def replace_spaces_with_underscores(input_string):
        return input_string.replace(" ", "_")

    # Since the Training name the user will input will have spaces it needs to have those spaces replaced with underscores so that the column titles match
    modified_string = replace_spaces_with_underscores(training_name)
    print(modified_string)

    # SQL query to select the number of non-null dates and dates that are less then the due date
    query_employees_who_have_not_completed_training = f"SELECT COUNT(*) AS count FROM employee_training WHERE {modified_string} IS NULL"

    # SQL query to select the total number of employees
    query_employee_count = "SELECT COUNT(*) AS count FROM employee_training"

    try:
        cursor.execute(query_employees_who_have_not_completed_training)
        
        # Fetch all rows of the query result
        # This will result in a list of tuples
        employee_completion = cursor.fetchall()

        cursor.execute(query_employee_count)

        # Fetch all rows of the query result
        # This will result in a list of tuples
        employee_count = cursor.fetchall()
    finally:
        # Close the cursor and connection to clean up
        cursor.close()
        conn.close()
    
    try:
        employee_percentage = (employee_completion[0][0] / employee_count[0][0]) * 100
    except ZeroDivisionError:
        return 400.0
    
    return employee_percentage


@action
def send_email_reminder(training_name: str) -> str:
    """
    Kicks off am email reminder bot in Sema4's Control Room and returns detailed information 
    about the number of and types of emails sent on your behalf.

    Args:
        training_name: name of the training you want to send reminder emails for

    Returns:
        str:  detailed information about the number of and types of emails sent on your behalf
    """
    # Define the path to your SQLite database
    database_path = 'training_database.db'

    # Create a connection to the database
    conn = sqlite3.connect(database_path)

    # Create a cursor object using the connection
    cursor = conn.cursor()

    def replace_spaces_with_underscores(input_string):
        return input_string.replace(" ", "_")
    
    modified_string = replace_spaces_with_underscores(training_name)

    # SQL query to select the number of non-null dates and dates that are less then the due date
    query_employees_who_need_to_complete_training = f"SELECT employees.employee_id, employees.name, employees.email, vacations.start_date, vacations.end_date FROM employee_training JOIN employees ON employees.employee_id = employee_training.employee_id LEFT JOIN vacations ON employee_training.employee_id = vacations.employee_id WHERE employee_training.{modified_string} IS NULL"

    try:
        cursor.execute(query_employees_who_need_to_complete_training)
        
        # Fetch all rows of the query result
        # This will result in a list of tuples
        deficient_employees = cursor.fetchall()

        total_count = 0
        sent = 0
        vacation = 0        
        today = datetime.today()

        for row in deficient_employees:
            total_count += 1
            if row[4] is not None:
                date_format = "%Y-%m-%d"
                vacation_start = datetime.strptime(row[4], date_format)

                # need to create work item JSON here so I can send it to the RC process via API call
                if vacation_start <= today:
                    vacation += 1
                else:
                    sent += 1
            else:
                sent += 1
    finally:
        # Close the cursor and connection to clean up
        cursor.close()
        conn.close()

    result_string = f"There were a total of {total_count} emails sent to employees.\n Of the {total_count} that were sent {sent} were sent today and {vacation} will be sent when the employee returns from vacation."

    #   requests.request("post", "https://cloud.robocorp.com/api/v1/workspaces/a0362d18-0d0a-46e6-bbd5-4dc683910794/processes/297953bf-e40a-44ed-a1f7-50c1c565eb95/process-runs", headers={
    #   "Content-Type": "application/json",
    #   "Authorization": "RC-WSKEY 5thfFpdRLUP0m7zzJTceLRqt2I8sL8IAPHoCgGZQnL1hpqL8xP8xskcAxUyN25f57LlxlwuWgIrlcQ6kJdBbPSfIl2L8e6pdSDWiGhM6x9Z7oL4fYDSvR5Aqju5AqHfr"
    # }, json={})
    
    return result_string