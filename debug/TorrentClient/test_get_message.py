import unittest
from message import Message, \
                    KeepAlive, \
                    Choke, \
                    UnChoke, \
                    Interested, \
                    NotInterested, \
                    Have, \
                    BitField, \
                    Request, \
                    Piece, \
                    Cancel, \
                    Port

class TestGetMessage(unittest.TestCase):

    def test_keep_alive(self):
    	message = Message.get_message('keep-alive')
    	self.assertEqual(message, KeepAlive())

    def test_choke(self):
    	message = Message.get_message('choke')
    	self.assertEqual(message, Choke())

    def test_unchoke(self):
    	message = Message.get_message('unchoke')
    	self.assertEqual(message, UnChoke())

    def test_interested(self):
    	message = Message.get_message('interested')
    	self.assertEqual(message, Interested())

    def test_have(self):
    	message = Message.get_message('have', 0)
    	self.assertEqual(message, Have(0))
    
    def test_bitfield(self):
    	message = Message.get_message('bitfield', None, None, None, None, None, '1111111011111111')
    	self.assertEqual(message, BitField('1111111011111111'))

    def test_request(self):
    	message = Message.get_message('request', 0, 1, 2 ** 8)
    	self.assertEqual(message, Request(0, 1, 2 ** 8))

    def test_piece(self):
        message = Message.get_message('piece', 0, 0, None, b'0000111100001111')
        self.assertEqual(message, Piece(0, 0, b'0000111100001111'))

    def test_cancel(self):
        message = Message.get_message('cancel', 0, 1, 2 ** 8)
        self.assertEqual(message, Cancel(0, 1, 2 ** 8))

    def test_port(self):
        message = Message.get_message('port', None, None, None, None, 80)
        self.assertEqual(message, Port(80))


if __name__ == '__main__':
    unittest.main()