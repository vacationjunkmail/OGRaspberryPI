# import mysql.connector
from mysql.connector import (connection)  # MySQLConnector
from mysql.connector.cursor import MySQLCursorPrepared
from mysql.connector import Error
from mysql.connector.constants import ClientFlag

import configparser,datetime
from os.path import expanduser


def read_config_file(filename='.config.ini', section='mysql'):
    parser = configparser.ConfigParser()
    config_file = "/home/pi/{}".format(filename)
    parser.read(config_file, encoding="utf-8")

    data = {}

    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            data[item[0]] = item[1]
    else:
        raise Exception("{0} not found in {1}".format(section, config_file))

    return data


class get_connection():

    def __init__(self):
        self.db_config = read_config_file()
        self.conn = connection.MySQLConnection(**self.db_config)
        #a = "username={user}\npassword={password}".format(**self.db_config)
        #print(a)
        #for item in dir(self.conn):
            #print(item)
        #print(self.conn._server_version)
        self.curr = self.conn.cursor(cursor_class=MySQLCursorPrepared)

    def select_query(self, query):
        self.curr.execute(query)
        columns = self.curr.column_names

        return self.curr

    def insert_statement(self,query,params):
        try:
            self.conn.start_transaction()
            self.curr.execute('''insert into test_db.test_tbl(username,pwd)values("manualinsert","pwd_insert");''')
            self.curr.execute(query,params)
            self.conn.commit()
            return "insert was good"
        except Error as err:
            self.conn.rollback()
            return err

    def close_connection(self):
        self.conn.close()
        return 'Goodbye'
	
    def select_params(self,query,params):
        columns = []
        data = []
        error = []
        try:
            self.curr.execute(query,params)
            columns = self.curr.column_names
            data = self.fetchresults(columns,self.curr.fetchall())
        except Exception as e:
            error.append(e)
        return columns,data,error

    def fetchresults(self,columns,query):
        data = []
        for recordset in query:
            c = 0
            d = {}
            for row_value in recordset:
                if type(row_value) == int:
                    d[columns[c]] = row_value
                elif type(row_value) == datetime.date:
                    d[columns[c]] = row_value.strftime('%Y-%m-%d')
                else:
                    try:
                        d[columns[c]] = row_value.decode()
                    except:
                        d[columns[c]] = row_value
                c +=1
            data.append(d)
        return data
