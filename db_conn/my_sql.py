#import mysql.connector
from mysql.connector import (connection) #MySQLConnector
from mysql.connector.cursor import MySQLCursorPrepared
import configparser
from os.path import expanduser

def read_config_file(filename = '.config.ini', section = 'mysql'):
    parser = configparser.ConfigParser()
    config_file = "{}/{}".format(expanduser("~"),filename)
    parser.read(config_file,encoding = "utf-8")

    data = {}
    print(config_file)

    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            data[item[0]] = item[1]
    else:
        raise Exception("{0} not found in {1}".format(section,config_file))

    #print(data)

    return data

class get_connection():
    def __init__(self):
        self.db_config = read_config_file()
        self.conn = connection.MySQLConnection(**self.db_config)
        self.curr = self.conn.cursor(cursor_class = MySQLCursorPrepared)

    def select_query(self,query):
        self.curr.execute(query)
        return self.curr

    def close_connection(self):
        self.conn.close()
        return 'Goodbye'

