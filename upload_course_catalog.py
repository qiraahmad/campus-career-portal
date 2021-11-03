import psycopg2
import csv, sys, ast
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

# use Python's open() function to load the CSV data
with open('./data/Course Data.csv') as csv_file:
   csv_reader = csv.reader(csv_file, delimiter=',')
   line_count = 0
   for row in csv_reader:
      line_count += 1
      if line_count > 1 and line_count < 43:
         if row[2] == '':
            row[2] = None
         if row[3] == '':
            row[3] = None
         sql_string = '''INSERT INTO public."Course_Catalog"
         ("Course_Code", "Course_Title", "Related_Course", "Course_Type", "Course_Details")
         VALUES (%s, %s, %s, %s, %s)
         '''
         cursor.execute(sql_string, (row[0], row[1], row[2], row[3], row[4]))
         conn.commit()
 

      elif line_count == 43:
         break
   print(f'Processed {line_count - 1} lines.')

#Closing the connection
conn.close()