__author__ = 'xsank'

import logging
import traceback
import tornado.websocket

from daemon import Bridge
from data import ClientData
from utils import check_ip, check_port

import itchat
from itchat.content import *

global client
client=1
global author
author=1

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WSHandler(tornado.websocket.WebSocketHandler):
    @staticmethod
    def get_client():
        return client

    def put_client(self):
        global client 
        client = Bridge(self)
        global author
        author = itchat.search_friends(nickName=r'sdserver')[0]
        author.send("hand")
        client.trans_back("\r\n connected \r\n")

    def remove_client(self):
        return

    @staticmethod
    def _check_init_param(data):
        return True

    @staticmethod
    def _is_init_data(data):
        return data.get_type() == 'init'

    def _id(self):
        return id(self)

    def open(self):
        self.put_client()

    def on_message(self, message):
        bridge = self.get_client()

    @itchat.msg_register([itchat.content.TEXT])
    def wechat_onmessage(msg):
        if msg['Type'] == TEXT:
            output=""
            try:
                if client == 1 :
                    print("open your web browser")
                    return
                if msg['Content'].startswith('pi'):
                    print(msg['Content'])
                    client.trans_back(msg['Content'])
                elif msg['Content']=='hand':
                    status=0
                    output='welcome '+msg['FromUserName']
                    client.trans_back(output + "\r\n")
            except Exception,e:
                print("error wx client")
                print 'traceback.print_exc():'; traceback.print_exc()
                return

    def on_close(self):
        self.remove_client()
        logging.info('client close the connection: %s' % self._id())

