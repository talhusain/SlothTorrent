"""
This module will handle establishing the connection to the database
and pass the connection to objects that use it.
"""

import configparser
import psycopg2
import os
from bencoding.bencode import decode
from TorrentClient.torrent import Torrent
import datetime

DEBUG = True


class Database(object):
    '''
    Note that no calls to the self._connection should be made directly.
    If a method needs called it should be called on the instance of this
    class. If it only exists for the _connection object a wrapper will
    need created.
    '''

    def __init__(self, settings_file):

        # Parse config file to read in settings
        config = configparser.ConfigParser()
        config.read(settings_file)
        self.username = config['DATABASE']['username']
        self.password = config['DATABASE']['password']
        self.ip = config['DATABASE']['ip']
        self.port = config['DATABASE']['port']
        self.db_name = config['DATABASE']['db']

        # Establish connection object initialize tables
        # self._drop_all_tables()
        self._initialize_tables()
        # self.add_fake_plugin()
        # self.remove_plugin("https://github.com/BadStreff/slothtorrent_yts")
        # self._add_fake_torrents()
        # self._add_sample_torrents()
        self._connection.close()

    def _drop_all_tables(self):
        self._connection = self.get_connection()
        cursor = self._connection.cursor()
        cursor.execute(("DROP TABLE IF EXISTS torrents, "
                        "plugins, "
                        "announcers, "
                        "torrent_files"))
        self._connection.commit()
        self._connection.close()

    def _initialize_tables(self):
        self._connection = self.get_connection()
        cursor = self._connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS plugins"
                       "(url TEXT PRIMARY KEY, last_run TIMESTAMP)")
        cursor.execute("CREATE TABLE IF NOT EXISTS torrents "
                       "(info_hash BYTEA PRIMARY KEY,"
                       "name TEXT,"
                       "comment TEXT,"
                       "created_by TEXT,"
                       "creation_time TIMESTAMP,"
                       "piece_length INT,"
                       "pieces BYTEA,"
                       "provider TEXT REFERENCES plugins (url) "
                       "ON UPDATE CASCADE ON DELETE CASCADE)")
        cursor.execute("CREATE TABLE IF NOT EXISTS announcers "
                       "(url TEXT,"
                       "info_hash BYTEA REFERENCES torrents (info_hash) "
                       "ON UPDATE CASCADE ON DELETE CASCADE,"
                       "PRIMARY KEY (url, info_hash))")
        cursor.execute("CREATE TABLE IF NOT EXISTS torrent_files "
                       "(file_path TEXT,"
                       "length TEXT,"
                       "info_hash BYTEA REFERENCES torrents (info_hash) "
                       "ON UPDATE CASCADE ON DELETE CASCADE,"
                       "PRIMARY KEY (file_path, info_hash))")
        cursor.execute("CREATE TABLE IF NOT EXISTS users "
                       "(username TEXT PRIMARY KEY, password TEXT)")
        self._connection.commit()
        self._connection.close()

    def add_fake_plugin(self):
        self._connection = self.get_connection()
        cursor = self._connection.cursor()
        dt = datetime.datetime.now()
        cursor.execute(("INSERT INTO plugins VALUES "
                        "(%s, %s) "
                        "ON CONFLICT (url) DO NOTHING"),
                       ('None', dt))
        cursor.execute(("INSERT INTO plugins VALUES "
                        "(%s, %s) "
                        "ON CONFLICT (url) DO NOTHING"),
                       ('https://github.com/BadStreff/slothtorrent_yts', dt))
        self._connection.commit()
        self._connection.close()

    def _add_sample_torrents(self):
        print('importing sample torrents...')
        for file in os.listdir('sample_torrents'):
            with open('sample_torrents/' + file, 'rb') as f:
                torrent_dict = decode(f.read())
                torrent = Torrent(torrent_dict)
                self.import_torrent(torrent, 'None')

    def get_recent_torrents(self, number=10):
        """Returns a list of the most recently added torrents. If the
        number exceeds the total number of torrents in the database all
        torrents will be returned.
        ex SELECT * FROM News ORDER BY date DESC
        Args:
            number (int): The maximum number of torrents to return

        Returns:
            list: A list of Torrent objects
        """
        crit = 'info_hash,name,comment,created_by,creation_time,provider'
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(("SELECT " + crit + " FROM torrents ORDER BY "
                            "creation_time DESC limit %s"),
                           (number,))
            ret = cursor.fetchall()
        except psycopg2.ProgrammingError as e:
            print(e)
            connection.rollback()
            ret = []
        return ret

    def get_popular_torrents(self, number):
        """Returns torrents with the most seeders. If the number exceeds
        the total number of torrents in the database all torrents will
        be returned.

        Args:
            number (int): The maximum number of torrents to return

        Returns:
            list: A list of Torrent objects
        """
        pass

    def search_torrents(self, search_string):
        """Searches through all torrents based on a string

        Args:
            search_string (string): The string that determines the
            query.

        Returns:
            list: A list of Torrent objects
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(("SELECT * FROM torrents where name like %s "
                            "and comment like %s "),
                           (search_string, search_string))
            ret = cursor.fetchall()
        except psycopg2.ProgrammingError as e:
            print(e)
            connection.rollback()
            ret = []
        return ret

    def import_torrent(self, torrent, provider):
        """Imports a torrent object into the database. This function
        should only be called by the plugin module once in production

        Args:
            torrent (Torrent): Torrent object see torrent.py for more
            information
            provider (string): The url of the plugin that created the
            torrent

        Returns:
            BOOL: success or failure
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(("INSERT INTO torrents VALUES "
                            "(%s, %s, %s, %s, %s, %s, %s, %s) "
                            "ON CONFLICT (info_hash) DO NOTHING"),
                           (torrent.info_hash,
                            torrent.name,
                            torrent.comment,
                            torrent.created_by,
                            torrent.creation_date,
                            torrent.piece_length,
                            torrent.pieces,
                            provider))
            for tracker in torrent.trackers:
                cursor.execute(("INSERT INTO announcers VALUES (%s, %s) "
                                "ON CONFLICT (url, info_hash) DO NOTHING"),
                               (tracker, torrent.info_hash))
            for file in torrent.files:
                cursor.execute(("INSERT INTO torrent_files VALUES "
                                "(%s, %s, %s) "
                                "ON CONFLICT (file_path, info_hash) "
                                "DO NOTHING"),
                               (file['path'],
                                str(file['length']),
                                torrent.info_hash))
            ret = True
        except psycopg2.ProgrammingError as e:
            print(e)
            connection.rollback()
            ret = False
        cursor.close()
        connection.commit()
        connection.close()
        return ret

    def get_torrent(self, info_hash):
        """Returns a torrent from the database given an info_hash

        Args:
            info_hash (bytes): The info_hash of the torrent we want

        Returns:
            Torrent: see torrent.py for more information
        """

        connection = self.get_connection()
        cursor = connection.cursor()
        SQL = "SELECT * FROM torrents WHERE info_hash = %s;"
        try:
            cursor.execute(SQL, (info_hash,))
            tup = cursor.fetchone()
        except psycopg2.ProgrammingError as e:
            print(e)
            return None

        SQL = "SELECT * FROM torrent_files WHERE info_hash = %s;"
        try:
            cursor.execute(SQL, (info_hash,))
            torrent_files = cursor.fetchall()
        except psycopg2.ProgrammingError as e:
            print(e)
            return None

        SQL = "SELECT url FROM announcers WHERE info_hash = %s;"
        try:
            cursor.execute(SQL, (info_hash,))
            urls = cursor.fetchall()
        except psycopg2.ProgrammingError as e:
            print(e)
            return None
        connection.close()

        torrent_dict = {b'comment': tup[2].encode("utf-8"),
                        b'created by': tup[3].encode("utf-8"),
                        b'creation_date': tup[4].timestamp(),
                        b'announce-list': [[u[0].encode("utf-8")]
                                           for u in urls],
                        b'info': {b'name': tup[1].encode("utf-8"),
                                  b'piece length': tup[5],
                                  b'pieces': bytes(tup[6]),
                                  b'files': []
                                  }
                        }
        # this can also be done with list comprehension but looks a bit
        # cleaner in this format
        for file in torrent_files:
            file_dict = {b'path': [file[0].encode("utf-8")],
                         b'length': int(file[1])}
            torrent_dict[b'info'][b'files'].append(file_dict)

        return Torrent(torrent_dict)

    def add_plugin(self, url, last_run):
        """Add a plugin URL to the database

        Args:
            url (string): Full patch a .git repo that is the plugin

        Returns:
            BOOL: success or failure
        """

        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(("INSERT INTO plugins VALUES (%s, %s) "
                            "ON CONFLICT (url) DO NOTHING"),
                           (url, last_run))
        except psycopg2.ProgrammingError as e:
            print(e)
            return False
        connection.commit()
        cursor.close()
        connection.close()
        return True

    def remove_plugin(self, url):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM plugins WHERE url = %s", (url,))

        except psycopg2.ProgrammingError as e:
            print(e)
            return False
        connection.commit()
        connection.close()
        return True

    def get_all_plugins(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM plugins")
            return cursor.fetchall()
        except psycopg2.ProgrammingError as e:
            print(e)
        connection.close()
        return []

    def get_connection(self):
        return psycopg2.connect(user=self.username,
                                password=self.password,
                                host=self.ip,
                                port=int(self.port),
                                database=self.db_name)

    def verifyUsers(self,username,password):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = '%s'" % (username,))
            row = cursor.fetchone()
            if row[0] == username and row[1] == password:
                r = True
            r = False
        except:
            r = False
        connection.close()
        return r


if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=2)

    db = Database('settings.conf')
    torrent = db.get_torrent(b'\xf7\xfb\xaa\x14\x90\x97yE\xcf\xd5\xb8\x18\xb3\xcd\xb16\xce\xfd\xcb\x8e')
    pp.pprint('name: %s' % torrent.name)
    pp.pprint('info_hash: %s' % torrent.info_hash)
    pp.pprint('comment: %s' % torrent.comment)
    pp.pprint('status: %s' % torrent.status)
    # pp.pprint('pieces: %s' % torrent.pieces)
    pp.pprint('piece_length: %s' % torrent.piece_length)
    pp.pprint('created_by: %s' % torrent.created_by)
    pp.pprint('creation_date: %s' % torrent.creation_date)
    pp.pprint('encoding: %s' % torrent.encoding)
    pp.pprint('files: %s' % torrent.files)
    pp.pprint('length: %s' % torrent.length)
    pp.pprint('trackers: %s' % torrent.trackers)
    pp.pprint('total_pieces: %s' % torrent.total_pieces)
    pp.pprint('bitfield: %s' % torrent.bitfield)
