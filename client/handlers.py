from __future__ import print_function
import logging
import traceback
import tornado.websocket

from daemon import Bridge
from data import ClientData
import json
from utils import check_ip, check_port


import itchat
from itchat.content import *
import binascii

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
        content="_._hand_._connect"
        #content = binascii.hexlify("_._hand_._connect".encode('utf-8'))
        author.send(content)

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
        if author==1:
            return
        msgdata = json.loads(message)['data']
        if not isinstance(msgdata,dict):
            author.send("_._data_._" + msgdata)

    @itchat.msg_register([itchat.content.TEXT])
    def wechat_onmessage(msg):
        if msg['Type'] == TEXT:
            output=""
            try:
                if client == 1 :
                    print("open your web browser")
                    return
                if author['UserName']!=msg['FromUserName']:
                    return 
                msg['Content'] = binascii.unhexlify(msg['Content'])
                if msg['Content'].startswith('_._data_._'):
                    output=msg['Content'].split('_._data_._')[1]
                    client.trans_back( output )
            except Exception,e:
                print("error wx client")
                return

    def on_close(self):
        self.remove_client()
        logging.info('client close the connection: %s' % self._id())

