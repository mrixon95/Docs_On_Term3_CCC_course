import psycopg2

try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "postgres",
                                  host = "54.237.100.36",
                                  port = "5432",
                                  database = "postgres")

    print("BLAH")

    cursor = connection.cursor()

    my_query = '''CREATE TABLE Patient(
        PatientId INTEGER PRIMARY KEY,
        PatientFName VARCHAR,
        PatientLName VARCHAR,
        PateintSuburb VARCHAR
    '''

    cursor.execute(my_query)

    print("PostgreSQL Patient table created")


except (Exception, psycopg2.Error) as error:
    print ("Error while connecting to PostgreSQL", error)

finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")