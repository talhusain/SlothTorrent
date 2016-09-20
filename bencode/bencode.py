'''
Bencoding

Bencoding is a way to specify and organize data in a terse format. It supports the following types: byte strings, integers, lists, and dictionaries.
Byte Strings

Byte strings are encoded as follows: <string length encoded in base ten ASCII>:<string data>
Note that there is no constant beginning delimiter, and no ending delimiter.

    Example: 4: spam represents the string "spam"
    Example: 0: represents the empty string ""

Integers

Integers are encoded as follows: i<integer encoded in base ten ASCII>e
The initial i and trailing e are beginning and ending delimiters.

    Example: i3e represents the integer "3"
    Example: i-3e represents the integer "-3"

i-0e is invalid. All encodings with a leading zero, such as i03e, are invalid, other than i0e, which of course corresponds to the integer "0".

    NOTE: The maximum number of bit of this integer is unspecified, but to handle it as a signed 64bit integer is mandatory to handle "large files" aka .torrent for more that 4Gbyte.

Lists

Lists are encoded as follows: l<bencoded values>e
The initial l and trailing e are beginning and ending delimiters. Lists may contain any bencoded type, including integers, strings, dictionaries, and even lists within other lists.

    Example: l4:spam4:eggse represents the list of two strings: [ "spam", "eggs" ]
    Example: le represents an empty list: []

Dictionaries

Dictionaries are encoded as follows: d<bencoded string><bencoded element>e
The initial d and trailing e are the beginning and ending delimiters. Note that the keys must be bencoded strings. The values may be any bencoded type, including integers, strings, lists, and other dictionaries.
Keys must be strings and appear in sorted order (sorted as raw strings, not alphanumerics). The strings should be compared using a binary comparison, not a culture-specific "natural" comparison.

    Example: d3:cow3:moo4:spam4:eggse represents the dictionary { "cow" => "moo", "spam" => "eggs" }
    Example: d4:spaml1:a1:bee represents the dictionary { "spam" => [ "a", "b" ] }
    Example: d9:publisher3:bob17:publisher-webpage15:www.example.com18:publisher.location4:homee represents { "publisher" => "bob", "publisher-webpage" => "www.example.com", "publisher.location" => "home" }
    Example: de represents an empty dictionary {}
'''

class Bencode(object):
    '''
    All strings are expected to be byte strings. ie: b'test' not 'test'
    '''
    def encode(data):
        pass
    def decode(data):
        pass
    def _tokenize(data):
        """ Returns the bencode data in a tokenized list. """

        if data is None or data == b'':
            return []

        ret = []
        data = [bytes([b]) for b in data]

        for index, b in enumerate(data, start=0):
            print(index)
            print(b)
            print(b''.join(data[index:]))

            if b == b'd':
                return [b'd'] + Bencode._tokenize(b''.join(data[index+1:]))

            elif b == b'i':
                offset = 1
                while data[offset] != b'e':
                    offset += 1
                return [b'i'] + [b''.join(data[1:offset])] + Bencode._tokenize(b''.join(data[offset:]))

            elif b == b'l':
                return [b'l'] + Bencode._tokenize(b''.join(data[index+1:]))

            elif b.isdigit():
                offset = 1
                while data[offset].isdigit():
                    offset += 1
                val = int(b''.join(data[:offset]).decode())
                return [b''.join(data[:offset])] + [b':'] + [b''.join(data[offset+1:offset+val+1])] + Bencode._tokenize(b''.join(data[offset+val+1:]))

            elif b == b'e':
                try:
                    return [b'e'] + Bencode._tokenize(b''.join(data[index+1:]))
                except:
                    return [b'e']

            elif b == b':':
                return [b':'] + Bencode._tokenize(b''.join(data[index+1:]))

            else:
                raise ValueError
