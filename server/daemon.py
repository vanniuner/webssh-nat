__author__ = 'vanniuner'

import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException

class Bridge(object):
    def __init__(self, itchat , fromUserName):
        self._itchat = itchat
        self._fromUserName = fromUserName
        self._shell = None
        self._id = 0
        self.ssh = paramiko.SSHClient()

    @property
    def id(self):
        return self._id

    @property
    def itchat(self):
        return self._itchat

    @property
    def fromUserName(self):
        return self._fromUserName

    @property
    def shell(self):
        return self._shell

    def privaterKey(self, _PRIVATE_KEY, _PRIVATE_KEY_PWD):
        try:
            pkey = paramiko.RSAKey.from_private_key(StringIO(_PRIVATE_KEY), _PRIVATE_KEY_PWD)
        except paramiko.SSHException:
            pkey = paramiko.DSSKey.from_private_key(StringIO(_PRIVATE_KEY), _PRIVATE_KEY_PWD)
        return pkey

    def isPassword(self, data):
        return data.get("ispwd", True)

    def open(self, data={}):
        self.ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
        try:
            if self.isPassword(data):
                self.ssh.connect(
                    hostname=data["host"],
                    port=int(data["port"]),
                    username=data["username"],
                    password=data["secret"],
                )

            else:
                self.ssh.connect(
                    hostname=data["host"],
                    port=int(data["port"]),
                    username=data["username"],
                    pkey=self.privaterKey(data["secret"], None)
                )

        except AuthenticationException:
            raise Exception("auth failed user:%s ,passwd:%s" %
                            (data["username"], data["secret"]))
        except SSHException:
            raise Exception("could not connect to host:%s:%s" %
                            (data["hostname"], data["port"]))

        self.establish()

    def establish(self, term="xterm"):
        self._shell = self.ssh.invoke_shell(term)
        self._shell.setblocking(0)

        self._id = self._shell.fileno()
        IOLoop.instance().register(self)
        IOLoop.instance().add_future(self.trans_back())

    def trans_forward(self, data=""):
        if self._shell:
            self._shell.send(data)

    def trans_back(self):
        yield self.id
        connected = True
        while connected:
            result = yield
            if self._itchat:
                try:
                    self._itchat.send(u'%s' % result, self._fromUserName)
                except Exception:
                    connected = False
                if result.strip() == 'logout':
                    connected = False
        self.destroy()

    def destroy(self):
        self.ssh.close()
