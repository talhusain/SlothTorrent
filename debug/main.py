"""
This file will be the entry point of the programs. It will handle events that
should happen only once on start up and initializing the Request Handlerobject.
"""

from db import Database
from request_handler import RequestHandler
from TorrentClient.client import Client
import plugin


def main():
    # Initialize db handler with settings file
    db = Database('settings.conf')

    # Initialize Plugin Loader Object so it can load plugins and start
    # populating the database
    plugin.Loader(db, 'settings.conf')

    client = Client()

    # Initialize the request handler and start taking http requests
    RequestHandler(db, client)


if __name__ == '__main__':
    main()
