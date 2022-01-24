import nltk  
import psycopg2

# nltk.download('punkt')

#establishing the connection
conn = psycopg2.connect(
   database="campus_career_portal", user='postgres', password='123', host='127.0.0.1', port= '5432'
)
#Creating a cursor object using the cursor() method
cursor = conn.cursor()

def map_courses():
    # convert to lowercase
    query_string = '''	SELECT lower(CONCAT(cc."Course_Title", ' ', cc."Course_Details")) as course
	FROM public."Student_Courses" sc
	join public."Grades" g on g.id = sc.grade_id
	join Public."Course_Catalog" cc on sc.course_id = cc.id'''

    #Retrieving data
    cursor.execute(query_string)
    #Fetching 1st row from the table
    result = cursor.fetchall();
    res = list(map(' '.join, result))
    textsample = ' '.join([str(elem) for elem in res])

    query_string = '''SELECT name from public."Skills" where '{}' like CONCAT('%',lower(name),'%') '''.format(textsample)
    
    #Retrieving data
    cursor.execute(query_string)
    #Fetching 1st row from the table
    result = cursor.fetchall();
    res = [''.join(i) for i in result]
    print(res)

map_courses()