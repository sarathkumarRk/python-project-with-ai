from flask import Flask, request, jsonify
from flask_mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'student_db'

mysql = MySQL()
mysql.init_app(app)

# ---------- Add Student ----------
@app.post("/students")
def add_student():
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students(name, age, grade) VALUES(%s, %s, %s)",
                   (data["name"], data["age"], data["grade"]))
    conn.commit()
    return jsonify({"message": "Student added successfully!"})

# ---------- Get All Students ----------
@app.get("/students")
def get_students():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    result = cursor.fetchall()
    students = []
    for row in result:
        students.append({"id": row[0], "name": row[1], "age": row[2], "grade": row[3]})
    return jsonify(students)

# ---------- Get Student by ID ----------
@app.get("/students/<int:id>")
def get_student(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    row = cursor.fetchone()
    if row:
        return jsonify({"id": row[0], "name": row[1], "age": row[2], "grade": row[3]})
    return jsonify({"error": "Student not found"}), 404

# ---------- Update Student ----------
@app.put("/students/<int:id>")
def update_student(id):
    data = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET name=%s, age=%s, grade=%s WHERE id=%s",
        (data["name"], data["age"], data["grade"], id)
    )
    conn.commit()
    return jsonify({"message": "Student updated successfully!"})

# ---------- Delete Student ----------
@app.delete("/students/<int:id>")
def delete_student(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    return jsonify({"message": "Student deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
