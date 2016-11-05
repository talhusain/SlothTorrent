"""
This module will handle establishing the connection to the database
and pass the connection to objects that use it.
"""

import configparser
import psycopg2

DEBUG=True
import datetime
'''
conn = psycopg2.connect(database="test", user="postgres", password="secret")

The two call styles are mutually exclusive: you cannot specify connection parameters as keyword arguments together with a connection string; only the parameters not needed for the database connection (i.e. connection_factory, cursor_factory, and async) are supported together with the dsn argument.

The basic connection parameters are:

    dbname – the database name (only in the dsn string)
    database – the database name (only as keyword argument)
    user – user name used to authenticate
    password – password used to authenticate
    host – database host address (defaults to UNIX socket if not provided)
    port – connection port number (defaults to 5432 if not provided)

'''

class Database(object):
    '''
    Note that no calls to the self._connection should be made directly.
    If a method needs called it should be called on the instance of this class.
    If it only exists for the _connection object a wrapper will need created.
    '''
    def __init__(self, settings_file):

        # Parse config file to read in settings
        config = configparser.ConfigParser()
        config.read(settings_file)
        username = config['DATABASE']['username']
        password = config['DATABASE']['password']
        ip = config['DATABASE']['ip']
        port = config['DATABASE']['port']
        db_name = config['DATABASE']['db']

        # Establish connection object initialize tables
        self._connection = psycopg2.connect(user=username, 
                                            password=password,
                                            host=ip,
                                            port=int(port),
                                            database=db_name)
        self._initialize_tables()
        self._addFakeTorrents()

    def _initialize_tables(self):
        cursor = self._connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS plugins (url TEXT, last_run TIMESTAMP)")
        cursor.execute("CREATE TABLE IF NOT EXISTS torrents (info_hash BYTEA PRIMARY KEY, name TEXT, comment TEXT, created_by TEXT, creation_time TIMESTAMP, piece_length INT, pieces BYTEA)")
        cursor.execute("CREATE TABLE IF NOT EXISTS announcers (url TEXT, info_hash BYTEA REFERENCES torrents (info_hash), PRIMARY KEY (url, info_hash))")
        cursor.execute("CREATE TABLE IF NOT EXISTS torrent_files (file_path TEXT, length INT, info_hash BYTEA REFERENCES torrents (info_hash), PRIMARY KEY (file_path, length, info_hash))")
        self._connection.commit()

    def _addFakeTorrents(self):
        cursor = self._connection.cursor()
        dt = datetime.datetime.now()
        cursor.execute("INSERT INTO torrents VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (info_hash) DO NOTHING", (b'0000', 'sample0', 'sample comment', 'sample creator', dt, 0, b'0000'))
        cursor.execute("INSERT INTO torrents VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (info_hash) DO NOTHING", (b'0001', 'sample1', 'sample comment', 'sample creator', dt, 0, b'0000'))
        cursor.execute("INSERT INTO torrents VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (info_hash) DO NOTHING", (b'0002', 'sample2', 'sample comment', 'sample creator', dt, 0, b'0000'))
        cursor.execute("INSERT INTO torrents VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (info_hash) DO NOTHING", (b'0003', 'sample3', 'sample comment', 'sample creator', dt, 0, b'0000'))
        cursor.execute("INSERT INTO torrents VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (info_hash) DO NOTHING", (b'0004', 'sample4', 'sample comment', 'sample creator', dt, 0, b'0000'))
        self._connection.commit()

    def execute(self, statement):
        return self._connection.execute(statement)