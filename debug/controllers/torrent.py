from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for


torrent_page = Blueprint('torrent_page', __name__)
db = None
client = None


class TorrentController(object):
    def __init__(self, database, torrent_client):
        global db
        global client
        db = database
        client = torrent_client


@torrent_page.route('/torrent')
def index():
    # utilize the torrent_client to get the current list of torrents in
    # progress
    x = db.get_torrent(b'\xf7\xfb\xaa\x14\x90\x97yE\xcf\xd5\xb8\x18\xb3\xcd\xb16\xce\xfd\xcb\x8e')
    client.start(x)
    torrents = list(client._sessions)
    return render_template('torrent.html', torrents=torrents)


@torrent_page.route('/torrent/cancel', methods=['POST'])
def cancel():
    # using the torrent_client object cancel the specified torrent,
    # we can probably expect the info hash to be sent, but need to make
    # sure we can send raw bytes over html and have flask capture them,
    # otherwise it may make more send to send the Torrent.__hash__()
    return redirect(url_for('torrent_page.index'))


@torrent_page.route('/torrent/resume', methods=['POST'])
def resume():
    # using the torrent_client object resume the specified torrent,
    # we can probably expect the info hash to be sent, but need to make
    # sure we can send raw bytes over html and have flask capture them,
    # otherwise it may make more send to send the Torrent.__hash__()
    return redirect(url_for('torrent_page.index'))


@torrent_page.route('/torrent/pause', methods=['POST'])
def pause():
    # using the torrent_client object pause the specified torrent,
    # we can probably expect the info hash to be sent, but need to make
    # sure we can send raw bytes over html and have flask capture them,
    # otherwise it may make more send to send the Torrent.__hash__()
    return redirect(url_for('torrent_page.index'))


@torrent_page.route('/torrent/add', methods=['POST'])
def add():
    # using the torrent_client object add the specified torrent,
    # we can probably expect the info hash to be sent, but need to make
    # sure we can send raw bytes over html and have flask capture them,
    # otherwise it may make more send to send the Torrent.__hash__()
    return redirect(url_for('torrent_page.index'))


@torrent_page.route('/torrent/retrieve', methods=['POST'])
def retrieve():
    # this on is going to be tricky, and will require some thought.
    # it may be implemented sometime in the future after the
    # presentation, the design docs say to zip it and serve the zipped
    # file but I'm not sure this is the best route
    return redirect(url_for('torrent_page.index'))
