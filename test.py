import sqlite3

# Connect to the SQLite database
try:
    connection = sqlite3.connect('/home/shagnik/Documents/HMA/instance/database.db')
    cursor = connection.cursor()

    # Print data from the 'patient' table
    print("\nData from the 'patient' table:")
    cursor.execute("SELECT * FROM patient")
    patient_data = cursor.fetchall()
    for row in patient_data:
        print(row)

    # Print data from the 'doctor' table
    print("\nData from the 'doctor' table:")
    cursor.execute("SELECT * FROM doctor")
    doctor_data = cursor.fetchall()
    for row in doctor_data:
        print(row)

    print("\nData from the 'diagnosis' table:")
    cursor.execute("SELECT * FROM diagnosis")
    doctor_data = cursor.fetchall()
    for row in doctor_data:
        print(row)

except sqlite3.Error as error:
    print("Error connecting to the database:", error)

finally:
    # Close the database connection
    if 'connection' in locals() and connection:
        connection.close()
        print("Database connection closed")
