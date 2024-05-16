import pymssql
import os

conn = pymssql.connect(
    server=os.environ['DB_SERVER'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    database='Test_db',
    as_dict=True
)

SQL_QUERY = """
SELECT * FROM Test_Table;
"""
cursor = conn.cursor()
cursor.execute(SQL_QUERY)
records = cursor.fetchall()
for r in records:
    print(f"{r['id']}\t{r['logging_time']}\t{r['is_alive']}")
print("Working propertly i guess")
conn.close()
