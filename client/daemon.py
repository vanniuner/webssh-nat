__author__ = 'xsank'

from tornado.websocket import WebSocketClosedError
import traceback

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class Bridge(object):
    def __init__(self, websocket):
        self._websocket = websocket
        self._id = 0

    @property
    def id(self):
        return self._id

    @property
    def websocket(self):
        return self._websocket

    def trans_forward(self, data=""):
        if author != 1:
            author.send(data)

    def trans_back(self,data=""):
        result = data
        if self._websocket:
            try:
                self._websocket.write_message(result)
            except WebSocketClosedError:
                print 'traceback.print_exc():'; traceback.print_exc()
                self.destroy()
            if result == 'logout':
                self.destroy()

    def destroy(self):
        self._websocket.close()
