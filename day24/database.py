import sqlite3

connection = sqlite3.connect('example.db')

#Create a cursor object to interact with the database
cursor = connection.cursor()

#Create a table named'employees'
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL
);
''')

connection.commit()

cursor.execute('''
INSERT INTO employees (name, position, department, salary)
VALUES (?, ?, ?, ?)
''', ('John Doe', 'Software Engineer', 'IT', 75000))

connection.commit()

cursor.execute('SELECT * FROM employees')

rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute('''
UPDATE employees
SET salary = ?
WHERE name = ?''', (30000, 'John Doe'))
connection.commit()

cursor.execute('''
DELETE FROM employees
WHERE name = ?''', ('John Doe',))

connection.commit()

cursor.close()
connection.close()