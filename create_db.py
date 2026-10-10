import getpass
import pymysql

# Amazon RDS MySQL connection details
DB_HOST = "pratikdb.crqy8s8e8fcl.ap-south-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = getpass.getpass("Enter the Password: ")
try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=3306,
        connect_timeout=10,
        autocommit=True
    )

    print("Connected to RDS successfully!")

    with connection.cursor() as cursor:
        # Create database
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS flaskdb"
        )
        print("Database flaskdb is ready.")

        # Select database
        cursor.execute("USE flaskdb")

        # Create table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL
            )
        """)

        print("Table users is ready.")
        print("Setup completed successfully!")

    connection.close()

except pymysql.MySQLError as error:
    print("Database error:", error)

