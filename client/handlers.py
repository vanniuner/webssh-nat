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

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WSHandler(tornado.websocket.WebSocketHandler):

    @itchat.msg_register([itchat.content.TEXT])
    def simple_reply(msg):
        if msg['Type'] == TEXT:
            output=""
            try:
                if client == 1 :
                    print("wait for init")
                    return
                else:
                    return
                bridge = client
                if msg['Content'].startswith('pi'):
                    print("local-ssh-connection")
                    bridge.trans_forward(msg['Content'])
                elif msg['Content']=='hand':
                    status=0
                    output='welcome '+msg['FromUserName']
            except Exception,e:
                print("error wx client")
                print 'traceback.print_exc():'; traceback.print_exc()
                return

    @staticmethod
    def get_client():
        return client

    def put_client(self):
        print("init bridge")
        client = Bridge(self)

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
        client_data = ClientData(message)
        if self._is_init_data(client_data):
            if self._check_init_param(client_data.data):
                logging.info('connection established from: %s' % self._id())
            else:
                self.remove_client()
                logging.warning('init param invalid: %s' % client_data.data)
        else:
            if bridge:
                bridge.trans_forward(client_data.data)

    def on_close(self):
        self.remove_client()
        logging.info('client close the connection: %s' % self._id())

