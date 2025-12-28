import sqlite3

db = sqlite3.connect("first.db")
cursor = db.cursor()

cursor.executescript("DROP TABLE IF EXISTS Ages;")
cursor.executescript(
    """
CREATE TABLE Ages (
    name VARCHAR(128),
    age INTEGER
);
"""
)

print("Enter SQL statements (empty line to finish):")

lines = []
while True:
    line = input()
    if line.strip() == "":
        break
    lines.append(line)

multi_input = "\n".join(lines)

cursor.executescript(multi_input)
db.commit()

cursor.execute("SELECT hex(name || age) AS X FROM Ages ORDER BY X")
print(cursor.fetchone()[0])

db.close()
