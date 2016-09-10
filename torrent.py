"""
NOTE: This is just an example of how I might intuitively go about beginning the boilerplate code and documentation
        for the Torrent class. Take it with a grain of salt. :)
        I welcome constructive criticism.

ALSO NOTE: Random, but I just discovered that the built-in function dir(m) returns a sorted list of strings containing 
             the names of all the modules, variables, and functions that are defined in a Python module m.

FILE: torrent.py
CLASS PROVIDED: Torrent

CONSTRUCTOR for the Torrent class:
  __init__(self, status, path, name, size, info, tracker_locations)
    __status:            <description of parameter>
    __path:              <description of parameter>
    .
    .
    .
    __tracker_locations: <description of parameter>
  Precondition: Member variables all have values that are within a specified set of values.
  Postcondition: The torrent has been initialized in a particular state.

MODIFICATION MEMBER FUNCTIONS for the Torrent class:
  set_status(self, status)

INVARIANT for the Torrent class:
  <enumerate constraints to be included in the class invariant>
"""

class Torrent:
	def __init__(self, status, path, name, size, info, tracker_locations):
        self.__status = status
        self.__path = path
        self.__name = name
        self.__size = size
        self.__info = info   # Did you have a certain domain of torrent characteristics in mind for "info," Adam?
        """ 
        Potentially a list (or tuple, sequence, or whatnot) of network locations for trackers (which, for those
          unaware, are "computers that help participants in the BitTorrent file distribution system find each other
          and form efficient distribution groups called 'swarms'" [en.wikipedia.org/wiki/Torrent_file]).
        """ 
        self.__tracker_locations = tracker_locations
        # etc...

	def set_status(self, status):
        self.__status = status

    def set_path(self, path):
        self.__path = path

    def set_name(self, name):
        self.__name = name

    def set_info(self, info):
        self.__info = info

    def get_status(self):
        return self.__status

    def get_path(self):
        return self.__path

    def get_name(self):
        return self.__name

    def get_info(self):
        return self.__info


