__author__ = 'vanniuner'

import os.path
import os
import signal

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import options

import itchat
from itchat.content import *

from config import init_config
from urls import handlers

import threading

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    server_wchat_user='@d82de0a67a363bfe7e1f77ae05216fe14af169ef76245dd726a5f0bcde42305b'
)
is_exit = 0
global itchat

class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, handlers, **settings)

def f(a,b):
    global is_exit
    is_exit=1
    print 'shutdown...'
    os.kill(os.getpid(),signal.SIGKILL)

def welcome(port):
    print('''
Welcome to the webssh!
                __              __
 _      _____  / /_  __________/ /_
| | /| / / _ \/ __ \/ ___/ ___/ __ \\ - nat-client
| |/ |/ /  __/ /_/ (__  |__  ) / / /
|__/|__/\___/_.___/____/____/_/ /_/

Now start~
Please visit the localhost:%s from the explorer~
    ''' % port)

def wechatAction():
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    itchat.run()

def main():
    init_config()
    options.parse_config_file("webssh.conf")
    signal.signal(signal.SIGINT,f)

    wxchat =threading.Thread(target=wechatAction)
    wxchat.start()

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    welcome(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
