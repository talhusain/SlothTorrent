"""
All plugin related logic should go here.
This file might eventually need broken into a seperate package,
depending on how complex it gets.
"""

import configparser
import os
import queue
from git import Repo
from urllib.parse import urlparse
# from db import Database
from pluginbase import PluginBase


class Loader(object):
    def __init__(self, db, settings_file):
        self._db = db
        self.settings_file = settings_file

        self._parse_config()
        self._load_plugins()

    def _load_plugins(self):
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
    loader = Loader(None, 'settings.conf')
    path = loader.clone_plugin('https://github.com/BadStreff/slothtorrent_yts')

    plugin_base = PluginBase(package='test')
    plugin_source = plugin_base.make_plugin_source(searchpath=[path])
    with plugin_source:
        src = plugin_source.load_plugin('main')
    q = queue.Queue()
    src.init(q)
