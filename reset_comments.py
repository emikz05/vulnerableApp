import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("DELETE FROM comments")

conn.commit()
conn.close()

print("comments reset successfully")
