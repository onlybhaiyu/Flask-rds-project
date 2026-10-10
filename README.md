# Flask RDS Project

A simple Flask web application hosted on AWS EC2 and connected to Amazon RDS MySQL to store user registration details.

## Technologies
- Python, Flask, PyMySQL
- AWS EC2, RDS MySQL, ALB
- VPC and Security Groups

## Project Files
- **`create_db.py`** — Creates the database and `users` table.
- **`app.py`** — Runs the registration form and saves user details to RDS.

## How to Run
```bash
pip install flask pymysql
python create_db.py
python app.py
```

Configure your RDS connection details before running. Keep database passwords out of GitHub.

