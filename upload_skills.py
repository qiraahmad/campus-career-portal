import psycopg2
import json, sys, ast
import pandas as pd    

#establishing the connection
conn = psycopg2.connect(
   database="campus_career_portal", user='postgres', password='123', host='127.0.0.1', port= '5432'
)

#Setting auto commit false
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Retrieving data
cursor.execute('''SELECT * from public."CSO"''')

#Fetching 1st row from the table
result = cursor.fetchall();
print(result)

#Commit your changes in the database
conn.commit()

# use Python's open() function to load the JSON data
with open('cleaned_related_skills.json') as json_data:
    for line in json_data:
        line = json.loads(line.strip())
        line = dict(line)
        for key, value in line.items():
          if value == None:
           line[key] = 'None'
        
        values = list(line.values())
        query_args = str(values).replace('[','(').replace(']',')')
        sql_string = '''INSERT INTO public."Skills" (name, related_1, related_2, related_3, related_4, related_5, related_6, related_7, related_8, related_9, related_10)'''
        sql_string += " VALUES {} ".format(query_args)
        cursor.execute(sql_string)
        conn.commit()

#Closing the connection
conn.close()