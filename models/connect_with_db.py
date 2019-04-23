from psycopg2 import connect

"""CREATE YOUR OWN DATABASE!!!!"""
def get_connection(user='', password='', host='', database='', port=):
    connection = connect(user=user, password=password, host=host, database=database, port=port)
    connection.autocommit = True
    return connection
