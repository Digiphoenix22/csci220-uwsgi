from flask import Flask, request, render_template, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Database connection info
DATABASE_URL = "postgres://yourusername:yourpassword@localhost:5432/yourdatabasename"

# Connect to your postgres DB
conn = psycopg2.connect(DATABASE_URL)

@app.route('/')
def home():
    return "Welcome to the University Web App!"

@app.route('/students')
def show_students():
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM student")
    students = cur.fetchall()
    cur.close()
    return render_template('students.html', students=students)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        
        cur = conn.cursor()
        cur.execute("INSERT INTO student (id, name) VALUES (%s, %s)", (id, name))
        conn.commit()
        cur.close()
        
        return redirect(url_for('show_students'))
    return render_template('add_student.html')


if __name__ == '__main__':
    app.run(debug=True)
