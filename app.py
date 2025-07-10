from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootroot",  # ← Replace with your real MySQL password
    database="student_db"
)
cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        cursor.execute("INSERT INTO students (name, email, course) VALUES (%s, %s, %s)", (name, email, course))
        db.commit()
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        cursor.execute("UPDATE students SET name=%s, email=%s, course=%s WHERE id=%s", (name, email, course, id))
        db.commit()
        return redirect('/')
    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()
    return redirect('/')
if __name__ == '_main_':
    app.run(debug=True,port=5001)