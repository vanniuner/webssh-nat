__author__ = 'xsank'

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

    def establish(self, term="xterm"):
        self._shell = self.ssh.invoke_shell(term)
        self._shell.setblocking(0)

        self._id = self._shell.fileno()

    def trans_forward(self, data=""):
        if self._shell:
            self._shell.send(data)

    def trans_back(self):
        yield self.id
        connected = True
        while connected:
            result = yield
            if self._websocket:
                try:
                    print("back:",result)
                    self._websocket.write_message(result)
                except WebSocketClosedError:
                    connected = False
                if result.strip() == 'logout':
                    connected = False
        self.destroy()

    def destroy(self):
        self._websocket.close()
