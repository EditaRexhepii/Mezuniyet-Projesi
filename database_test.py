import json

to_dump = [0,0,0,0,0,0,0,0,0,0]
sql_as_text = json.dumps(to_dump)
#
# print(type(sql_as_text))
#
# to_dump = json.loads(sql_as_text)
# print(type(to_dump))

import sqlite3

connection_obj = sqlite3.connect('database/users.db')

cursor_obj = connection_obj.cursor()

statement = """SELECT beginner FROM user_data WHERE name = ? """
t=('esat',)
# cursor_obj.execute(statement,t)
# statement = '''UPDATE user_data SET beginner= ? WHERE name= ?'''
# t=(sql_as_text,'esat',)
cursor_obj.execute(statement,t)
print("All the data")
output = cursor_obj.fetchall()
to_dump = json.loads(output[0][0])
print(to_dump)
to_dump[2]=2
print(to_dump)

# print(output)
connection_obj.commit()

# Close the connection
connection_obj.close()