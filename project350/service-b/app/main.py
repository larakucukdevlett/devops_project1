from flask import Flask, request, render_template_string
import psycopg2
import os

app = Flask(__name__)

DATABASE = {
    "host": os.getenv("DATABASE_HOST"),
    "dbname": os.getenv("DATABASE_NAME"),
    "user": os.getenv("DATABASE_USER"),
    "password": os.getenv("DATABASE_PASSWORD"),
}
def get_db_connection():
    conn = psycopg2.connect(**DATABASE)
    return conn
@app.route("/", methods=["GET","POST"])
def home():
    if request.method=="POST":
        first_name=request.form["first_name"]
        last_name=request.form["last_name"]
        conn=get_db_connection()
        cur=conn.cursor()
        #checking if name is already in database
        cur.execute("SELECT * FROM users WHERE first_name = %s AND last_name=%s",(first_name,last_name))
        user = cur.fetchone()
        if user:
            message="Name already exists."
        else:
            cur.execute("INSERT INTO users (first_name,last_name,created_at) VALUES (%s,%s,NOW())",(first_name,last_name))
            conn.commit()
            #total count of records.
            cur.execute("SELECT COUNT(*) FROM users")
            total_records = cur.fetchone()[0]
            message = f"Name added and Total records:{total_records}."
        cur.close()
        conn.close()
        return render_template_string("""
            <h1>{{ message }}</h1>
            <a href="/">Enter Another Record</a>
        """, message=message)

    return render_template_string("""
        <form method="POST">
            <label for="first_name">First Name</label>
            <input type="text" id="first_name" name="first_name" required>
            <br>
            <label for="last_name">Last Name</label>
            <input type="text" id="last_name" name="last_name" required>
            <br>
            <button type="submit">Submit</button>
        </form>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)