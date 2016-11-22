"""
All plugin related logic should go here.
This file might eventually need broken into a seperate package,
depending on how complex it gets.
"""

from db import Database
import configparser
import os
import threading
import queue
from git import Repo
from urllib.parse import urlparse
import requests
from torrent import Torrent
from bencoding.bencode import decode
from pluginbase import PluginBase


class Loader(object):
    def __init__(self, db, settings_file):
        self._db = db
        self._queue = queue.Queue()
        self.settings_file = settings_file
        self.sample_plugin = 'https://github.com/BadStreff/slothtorrent_yts'

        self._parse_config()
        threading.Thread(target=self._process_queue).start()
        threading.Thread(target=self._load_plugins).start()

    def _load_plugins(self):
        # clone the plugin into the directory that self.plugin_dir
        # points to, in this case the local plugins/ directory
        plugins = self._db.get_all_plugins()
        print(plugins)
        for plugin, last_run in plugins:
            try:
                path = self.clone_plugin(plugin)
            except:
                continue
            # setup our plugin base and add the cloned plugin to it
            plugin_base = PluginBase(package='plugins')
            plugin_source = plugin_base.make_plugin_source(searchpath=[path])
            # using the plugin_source we setup, this is the equivalent of:
            # from slothtorrent_yts import main
            if plugin == 'None':
                continue
            with plugin_source:
                src = plugin_source.load_plugin('main')
            # using main module from the slothtorrent_yts packe we imported:
            # start a new thread and run it's init() method passing it our
            # queue
            t = threading.Thread(target=src.init, args=(self._queue,))
            t.start()

    def _process_queue(self):
        while True:
            if not self._queue.empty():
                url = self._queue.get()
                # print('got url %s' % url)
                r = requests.get(url)
                try:
                    r = self._db.import_torrent(Torrent(decode(r.content)),
                                                self.sample_plugin)
                    if not r:
                        print('Error importing %s' % url)
                except Exception as e:
                    print(e)
                    print('Encountered an exception importing %s' % url)
                    pass

    def _parse_config(self):
        config = configparser.ConfigParser()
        config.read(self.settings_file)
        self.plugin_dir = config['PLUGINS']['directory']

    def clone_plugin(self, url):
        path = urlparse(url).path
        path = os.path.join(self.plugin_dir, path[1:])
        if not os.path.exists(path):
            Repo.clone_from(url, path)
        return path


if __name__ == '__main__':
    db = Database('settings.conf')
    Loader(db, 'settings.conf')
