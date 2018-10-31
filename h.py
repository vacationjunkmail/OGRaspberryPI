from db_conn.my_sql import get_connection


mysql_db = get_connection()
    
query = 'select * from dinner.menu;'

query = mysql_db.select_query(query)
columns = query.column_names
data = []
#data = dict(zip(row, query.fetchall()))
for recordset in query.fetchall():
    #print(row)
    #print(recordset.column_names)
    c = 0
    d = {}
    for row_value in recordset:
        #d = {}
        d[columns[c]] = row_value
        #data.append(dict(zip(columns[c],row_value)))
        c += 1
    data.append(d)

for row in data:
    print(row['date'])
mysql_db.close_connection()
