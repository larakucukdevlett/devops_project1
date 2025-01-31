from flask import Flask, render_template_string, redirect, url_for
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
#list of users and delete option
@app.route("/", methods=["GET"])
def home():
    conn=get_db_connection()
    cur=conn.cursor()
    #fetching all records from users db with their creation time
    cur.execute("SELECT id,first_name,last_name,created_at FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string("""
        <ul>
        {% for user in users %}
            <li>{{ user[0] }} - {{ user[1] }} {{ user[2] }} (Created at: {{ user[3] }})
                <a href="/delete/{{ user[0] }}">[x]</a>
            </li>
        {% endfor %}
        </ul>
        <p>Total Records: {{ users|length }}</p>
        <a href="/">Refresh</a>
    """, users=users)
@app.route("/delete/<int:user_id>", methods=["GET"])
def delete(user_id):
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s",(user_id,)) #deleting the selected record from db
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM users") #remaining count
    remaining_records=cur.fetchone()[0]
    cur.close()
    conn.close()
    return render_template_string("""
        <h1>Record Deleted</h1>
        <p>Remaining Records: {{ remaining_records }}</p>
        <a href="/">Go back to list</a>
    """, remaining_records=remaining_records)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)