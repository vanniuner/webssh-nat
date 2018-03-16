__author__ = 'xsank'

from tornado.websocket import WebSocketClosedError

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
        return

    def trans_back(self,data=""):
        connected = True
        while connected:
            result = data
            if self._websocket:
                try:
                    self._websocket.write_message(result)
                except WebSocketClosedError:
                    connected = False
                if result == 'logout':
                    connected = False
        self.destroy()

    def destroy(self):
        self._websocket.close()
