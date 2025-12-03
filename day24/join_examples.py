import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS courses(
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    student_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
    )
'''
)

cursor.execute("INSERT INTO students (name) VALUES ('Alice')")
cursor.execute("INSERT INTO students (name) VALUES ('Bob')")

cursor.execute("INSERT INTO courses (course_name, student_id) VALUES ('Math', 1)")
cursor.execute("INSERT INTO courses (course_name, student_id) VALUES ('Science', 1)")
cursor.execute("INSERT INTO courses (course_name, student_id) VALUES ('Art', 2)")

conn.commit()

cursor.execute('''
SELECT students.name, courses.course_name
FROM students
JOIN courses ON students.student_id = courses.student_id''')

rows = cursor.fetchall()
for row in rows:
    print(f"Student: {row[0]}, Course: {row[1]}")

conn.close()