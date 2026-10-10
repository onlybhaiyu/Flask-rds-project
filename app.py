
import os
import getpass
import pymysql
from flask import Flask, request, render_template_string

app = Flask(__name__)

# AWS RDS MySQL configuration
DB_HOST = "pratikdb.crqy8s8e8fcl.ap-south-1.rds.amazonaws.com"
DB_USER = "admin"
DB_NAME = "flaskdb"

DB_PASSWORD = os.environ.get("DB_PASSWORD")
if not DB_PASSWORD:
    DB_PASSWORD = getpass.getpass("Enter RDS password: ")


# Modern registration page
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudConnect | Registration</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            color: #edf2ff;
            background:
                radial-gradient(circle at top left, #253c74, transparent 45%),
                linear-gradient(135deg, #080d1b, #111a31);
        }

        .container {
            width: 100%;
            max-width: 470px;
            padding: 38px;
            border: 1px solid rgba(255,255,255,0.13);
            border-radius: 22px;
            background: rgba(18,28,51,0.96);
            box-shadow: 0 25px 70px rgba(0,0,0,0.35);
        }

        .logo {
            width: 58px;
            height: 58px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 17px;
            background: linear-gradient(135deg, #6689ff, #8d5cf6);
            font-size: 27px;
            margin-bottom: 24px;
        }

        .tag {
            color: #91a9ff;
            font-size: 12px;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }

        h1 {
            font-size: 29px;
            margin-bottom: 12px;
        }

        .subtitle {
            color: #aab6d0;
            line-height: 1.6;
            font-size: 14px;
            margin-bottom: 28px;
        }

        label {
            display: block;
            font-size: 13px;
            margin-bottom: 9px;
        }

        input {
            width: 100%;
            padding: 14px 15px;
            margin-bottom: 21px;
            border: 1px solid #34415f;
            border-radius: 10px;
            background: #0d1528;
            color: white;
            font-size: 15px;
            outline: none;
        }

        input:focus {
            border-color: #8299ff;
            box-shadow: 0 0 0 3px rgba(100,130,255,0.13);
        }

        button {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(90deg, #587cff, #8a5cf6);
            color: white;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            opacity: 0.9;
        }

        .message {
            padding: 14px;
            margin-bottom: 22px;
            border-radius: 10px;
            font-size: 14px;
            line-height: 1.5;
        }

        .error {
            color: #ffb4b4;
            background: rgba(239,68,68,0.12);
            border: 1px solid rgba(239,68,68,0.35);
        }

        .footer {
            margin-top: 27px;
            padding-top: 20px;
            border-top: 1px solid #293650;
            color: #8492ae;
            font-size: 12px;
            text-align: center;
        }

        .footer span {
            color: #8eacff;
        }
    </style>
</head>

<body>
    <main class="container">
        <div class="logo">✦</div>

        <div class="tag">CloudConnect Platform</div>
        <h1>Create your profile</h1>

        <p class="subtitle">
            Enter your details below. Your information will be
            securely stored in our cloud database.
        </p>

        {% if error %}
            <div class="message error" role="alert">
                {{ error }}
            </div>
        {% endif %}

        <form action="/submit" method="POST">
            <label for="name">Full name</label>
            <input
                type="text"
                id="name"
                name="name"
                placeholder="Enter your full name"
                maxlength="100"
                required
            >

            <label for="email">Email address</label>
            <input
                type="email"
                id="email"
                name="email"
                placeholder="you@example.com"
                maxlength="150"
                required
            >

            <button type="submit">Submit details →</button>
        </form>

        <div class="footer">
            Powered by <span>Flask + Amazon RDS MySQL</span>
        </div>
    </main>
</body>
</html>
"""


# Database connection
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=3306,
        connect_timeout=10,
        cursorclass=pymysql.cursors.DictCursor
    )


# Display the form
@app.route("/", methods=["GET"])
def home():
    return render_template_string(
        HTML,
        error=None
    )


# Save submitted data in RDS and display that record
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()

    if not name or not email:
        return render_template_string(
            HTML,
            error="Please enter both your name and email."
        ), 400

    connection = None

    try:
        connection = get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (name, email)
            )

            user_id = cursor.lastrowid

        connection.commit()

        return render_template_string("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport"
                      content="width=device-width, initial-scale=1.0">
                <title>Submission Successful</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background: #0b1120;
                        color: #edf2ff;
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        padding: 20px;
                    }
                    .card {
                        max-width: 460px;
                        width: 100%;
                        padding: 35px;
                        border-radius: 18px;
                        background: #121c33;
                        border: 1px solid #34415f;
                    }
                    .check {
                        color: #4ade80;
                        font-size: 42px;
                    }
                    h2 { margin: 15px 0; }
                    p {
                        padding: 9px 0;
                        overflow-wrap: anywhere;
                    }
                    .success { color: #86efac; }
                    a {
                        display: inline-block;
                        margin-top: 20px;
                        color: #a5baff;
                    }
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="check">✓</div>
                    <h2 class="success">
                        Your data has been submitted!
                    </h2>
                    <p>Your record was saved in RDS MySQL.</p>
                    <hr>
                    <p><strong>Record ID:</strong> {{ user_id }}</p>
                    <p><strong>Name:</strong> {{ name }}</p>
                    <p><strong>Email:</strong> {{ email }}</p>
                    <a href="/">← Back to registration form</a>
                </div>
            </body>
            </html>
        """, user_id=user_id, name=name, email=email), 200

    except pymysql.MySQLError:
        if connection:
            connection.rollback()

        app.logger.exception("Failed to save data to RDS")

        return """
            <h2>Unable to save your data</h2>
            <p>Please try again or check the application logs.</p>
            <a href="/">Back to form</a>
        """, 500

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

