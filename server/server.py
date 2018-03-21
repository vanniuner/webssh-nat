# -*- coding: utf-8 -*-
__author__ = 'vanniuner'

import itchat
from itchat.content import *
import sys
import traceback
from daemon import Bridge
from ioloop import IOLoop
import binascii

def welcome():
    print('''
Welcome to the webssh-nat!
                __              __
 _      _____  / /_  __________/ /_
| | /| / / _ \/ __ \/ ___/ ___/ __ \\  - nat-server
| |/ |/ /  __/ /_/ (__  |__  ) / / /
|__/|__/\___/_.___/____/____/_/ /_/     

Now started ...''')

global client
client=None

@itchat.msg_register([itchat.content.TEXT])
def simple_reply(msg):
    if msg['Type'] == TEXT:
    	output=""
    	try:
	    	if msg['Content'].startswith('_._data_._'):
	    		global client
    			client.trans_forward(msg['Content'].split('_._data_._')[1])
	    	elif msg['Content'].startswith('_._hand_._'):
	    		#ssh connect
	    		client = Bridge(itchat,msg['FromUserName'])
	    		dict = {'host': '127.0.0.1', 'port': 22, 'username':'hack','secret':'cantsay'}
	    		client.open(dict)
        except Exception,e:
			print 'traceback.print_exc():'; traceback.print_exc()
			return ""

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	welcome()
	IOLoop.instance().start()
	itchat.auto_login(enableCmdQR=2, hotReload=True)
	itchat.run()


