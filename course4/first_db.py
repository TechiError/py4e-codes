import sqlite3

db = sqlite3.connect("first.db")
cursor = db.cursor()
cursor.executescript("DROP TABLE IF EXISTS Ages")
cursor.executescript(
    """
CREATE TABLE Ages (
               name VARCHAR(128),
               age INTEGER
)"""
)
cursor.executescript(
    """
DELETE FROM Ages;
INSERT INTO Ages (name, age) VALUES ('Kia', 17);
INSERT INTO Ages (name, age) VALUES ('Seonag', 13);
INSERT INTO Ages (name, age) VALUES ('Elan', 34);
INSERT INTO Ages (name, age) VALUES ('Christine', 31);
"""
)
db.commit()

cursor.execute("SELECT hex(name || age) AS X FROM Ages ORDER BY X")

print(cursor.fetchone()[0])
db.close()
