import sqlite3
import json

try:
    conn = sqlite3.connect("opengeo.sqlite")
except FileNotFoundError:
    conn = sqlite3.connect("course4/geodata/opengeo.sqlite")
cur = conn.cursor()

cur.execute("SELECT * FROM Locations")
fhand = open("where.js", "w", -1, "utf-8")
fhand.write("myData = [\n")
count = 0
for row in cur:
    data = str(row[1].decode())
    try:
        js = json.loads(str(data))
    except:
        continue

    if len(js["features"]) == 0:
        continue

    try:
        lat = js["features"][0]["geometry"]["coordinates"][1]
        lng = js["features"][0]["geometry"]["coordinates"][0]
        where = js["features"][0]["properties"].get("display_name") or js["features"][
            0
        ]["properties"].get("address_line1")
        where = where.replace("'", "")
    except:
        print("Unexpected format")
        print(js)

    try:
        print(where, lat, lng)

        count = count + 1
        if count > 1:
            fhand.write(",\n")
        output = "[" + str(lat) + "," + str(lng) + ", '" + where + "']"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")
