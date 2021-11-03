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
    textsample ="machine learning"  
    textsample = textsample.lower()
    # convert to lowercase

    sentences = nltk.sent_tokenize(textsample)  
    words = nltk.word_tokenize(textsample)  
    sentences = [w for w in words if w.isalpha()]
    sentences.append(textsample)
    query_args = str(sentences).replace('[','(').replace(']',')')
    query_string = '''SELECT * from public."Skills" where name in {}'''.format(query_args)
    print(query_string)

    #Retrieving data
    cursor.execute(query_string)
    #Fetching 1st row from the table
    result = cursor.fetchall();
    print(result)

map_courses()