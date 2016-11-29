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
    	msg = Message.get_message('keep-alive')
    	self.assertEqual(isinstance(msg, KeepAlive), True)

    def test_keep_alive__length(self):
        msg = Message.get_message('keep-alive')
        self.assertEqual(msg.length, 0)

    def test_keep_alive__to_bytes(self):
        msg_b = Message.get_message('keep-alive').to_bytes()
        self.assertEqual(msg_b, b'\x00\x00\x00\x00')

    def test_choke(self):
    	msg = Message.get_message('choke')
    	self.assertEqual(isinstance(msg, Choke), True)

    def test_choke(self):
        msg_b = Message.get_message('choke').to_bytes()
        self.assertEqual(msg_b, b'\x00\x00\x00\x01\x00')

    def test_choke__length(self):
        msg = Message.get_message('choke')
        self.assertEqual(msg.length, 1)

    def test_choke__id(self):
        msg = Message.get_message('choke')
        self.assertEqual(msg.id, 0)

    def test_unchoke(self):
    	msg = Message.get_message('unchoke')
    	self.assertEqual(isinstance(msg, UnChoke), True)

    def test_unchoke__to_bytes(self):
        msg_b = Message.get_message('unchoke').to_bytes()
        self.assertEqual(msg_b, b'\x00\x00\x00\x01\x01')

    def test_unchoke__length(self):
        msg = Message.get_message('unchoke')
        self.assertEqual(msg.length, 1)

    def test_unchoke__id(self):
        msg = Message.get_message('unchoke')
        self.assertEqual(msg.id, 1)

    def test_interested(self):
    	msg = Message.get_message('interested')
    	self.assertEqual(isinstance(msg, Interested), True)

    def test_interested__to_bytes(self):
        msg_b = Message.get_message('interested').to_bytes()
        self.assertEqual(msg_b, b'\x00\x00\x00\x01\x02')

    def test_interested__length(self):
        msg = Message.get_message('interested')
        self.assertEqual(msg.length, 1)

    def test_interested__id(self):
        msg = Message.get_message('interested')
        self.assertEqual(msg.id, 2)

    def test_not_interested(self):
        msg = Message.get_message('not interested')
        self.assertEqual(isinstance(msg, NotInterested), True)

    def test_not_interested__to_bytes(self):
        msg_b = Message.get_message('not interested').to_bytes()
        self.assertEqual(msg_b, b'\x00\x00\x00\x01\x03')

    def test_not_interested__length(self):
        msg = Message.get_message('not interested')
        self.assertEqual(msg.length, 1)

    def test_not_interested__id(self):
        msg = Message.get_message('not interested')
        self.assertEqual(msg.id, 3)

    def test_have(self):
    	msg = Message.get_message('have', 0)
    	self.assertEqual(isinstance(msg, Have), True)

    def test_have__to_bytes(self):
        msg_b = Message.get_message('have', 0).to_bytes()
        self.assertEqual(msg_b, b'\x00\x00\x00\x05\x04\x00\x00\x00\x00')

    def test_have__length(self):
        msg = Message.get_message('have', 0)
        self.assertEqual(msg.length, 5)

    def test_have__id(self):
        msg = Message.get_message('have', 0)
        self.assertEqual(msg.id, 4)
    
    def test_bitfield(self):
    	msg = Message.get_message('bitfield', None, None, None, None, None, '1111111011111111')
    	self.assertEqual(isinstance(msg, BitField), True)

    def test_bitfield__to_bytes(self):
        bitfield = [2 * 4, 2 * 8]
        bitfield_b = b'\x00\x00\x00\x03\x05\x08\x10'
        msg_b = Message.get_message('bitfield', None, None, None, None, None, bitfield).to_bytes()
        self.assertEqual(msg_b, bitfield_b)

    def test_bitfield__length(self):
        bitfield = '1111111011111111'
        msg = Message.get_message('bitfield', None, None, None, None, None, bitfield)
        self.assertEqual(msg.length, 1 + len(bitfield))

    def test_bitfield__id(self):
        bitfield = '1111111011111111'
        msg = Message.get_message('bitfield', None, None, None, None, None, bitfield)
        self.assertEqual(msg.id, 5)

    def test_bitfield__bitfield(self):
        bitfield = '1111111011111111'
        msg = Message.get_message('bitfield', None, None, None, None, None, bitfield)
        self.assertEqual(msg.bitfield, bitfield)

    def test_request(self):
    	msg = Message.get_message('request', 0, 1, 2 ** 8)
    	self.assertEqual(msg, Request(0, 1, 2 ** 8))

    def test_request__to_bytes(self):
        bitfield = [2 * 4, 2 * 8]
        bitfield_b = b'\x00\x00\x00\x03\x05\x08\x10'
        msg_b = Message.get_message('bitfield', None, None, None, None, None, bitfield).to_bytes()
        self.assertEqual(msg_b, bitfield_b)

    def test_request__length(self):
        msg = Message.get_message('request', 0, 1, 2 ** 8)
        self.assertEqual(msg.length, 13)

    def test_request__id(self):
        msg = Message.get_message('request', 0, 1, 2 ** 8)
        self.assertEqual(msg.id, 6)

    def test_request__index(self):
        msg = Message.get_message('request', 0, 1, 2 ** 8)
        self.assertEqual(msg.index, 0)

    def test_request__begin(self):
        msg = Message.get_message('request', 0, 1, 2 ** 8)
        self.assertEqual(msg.begin, 1)

    def test_request__request_length(self):
        msg = Message.get_message('request', 0, 1, 2 ** 8)
        self.assertEqual(msg.request_length, 2 ** 8)

    def test_piece(self):
        block = b'0000111100001111'
        msg = Message.get_message('piece', 0, 0, None, block)
        self.assertEqual(isinstance(msg, Piece), True)

    def test_piece__to_bytes(self):
        block = b'0000111100001111'
        block_b = b'\x00\x00\x00\x19\x07\x00\x00\x00\x00\x00\x00\x00\x000000111100001111'
        msg_b = Message.get_message('piece', 0, 0, None, block).to_bytes()
        self.assertEqual(msg_b, block_b)

    def test_piece__length(self):
        block = b'0000111100001111'
        msg = Message.get_message('piece', 0, 0, None, block)
        self.assertEqual(msg.length, 9 + len(block))

    def test_piece__id(self):
        block = b'0000111100001111'
        msg = Message.get_message('piece', 0, 0, None, block)
        self.assertEqual(msg.id, 7)

    def test_piece__index(self):
        block = b'0000111100001111'
        msg = Message.get_message('piece', 0, 0, None, block)
        self.assertEqual(msg.index, 0)

    def test_piece__begin(self):
        block = b'0000111100001111'
        msg = Message.get_message('piece', 0, 0, None, block)
        self.assertEqual(msg.begin, 0)

    def test_piece__block(self):
        block = b'0000111100001111'
        msg = Message.get_message('piece', 0, 0, None, block)
        self.assertEqual(msg.block, block)

    def test_cancel(self):
        msg = Message.get_message('cancel', 0, 1, 2 ** 8)
        self.assertEqual(isinstance(msg, Cancel), True)

    def test_cancel__to_bytes(self):
        cancel_b = b'\x00\x00\x00\r\x08\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x00'
        msg_b = Message.get_message('cancel', 0, 1, 2 ** 8).to_bytes()
        self.assertEqual(msg_b, cancel_b)

    def test_cancel__length(self):
        msg = Message.get_message('cancel', 0, 1, 2 ** 8)
        self.assertEqual(msg.length, 13)

    def test_cancel__id(self):
        msg = Message.get_message('cancel', 0, 1, 2 ** 8)
        self.assertEqual(msg.id, 8)

    def test_cancel__index(self):
        msg = Message.get_message('cancel', 0, 1, 2 ** 8)
        self.assertEqual(msg.index, 0)

    def test_cancel__begin(self):
        msg = Message.get_message('cancel', 0, 1, 2 ** 8)
        self.assertEqual(msg.begin, 1)

    def test_cancel__request_length(self):
        msg = Message.get_message('cancel', 0, 1, 2 ** 8)
        self.assertEqual(msg.request_length, 2 ** 8)

    def test_port(self):
        msg = Message.get_message('port', None, None, None, None, 80)
        self.assertEqual(isinstance(msg, Port), True)

    def test_port__to_bytes(self):
        port_b = b'\x00\x00\x00\x03\t\x00P'
        msg_b = Message.get_message('port', None, None, None, None, 80).to_bytes()
        self.assertEqual(msg_b, port_b)

    def test_port__length(self):
        msg = Message.get_message('port', None, None, None, None, 80)
        self.assertEqual(msg.length, 3)

    def test_port__id(self):
        msg = Message.get_message('port', None, None, None, None, 80)
        self.assertEqual(msg.id, 9)

    def test_port__listen_port(self):
        msg = Message.get_message('port', None, None, None, None, 80)
        self.assertEqual(msg.listen_port, 80)


if __name__ == '__main__':
    unittest.main()