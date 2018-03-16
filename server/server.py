__author__ = 'vanniuner'

import itchat
from itchat.content import *
import sys

def welcome():
    print('''
Welcome to the webssh-nat!
                __              __
 _      _____  / /_  __________/ /_
| | /| / / _ \/ __ \/ ___/ ___/ __ \\  - nat-server
| |/ |/ /  __/ /_/ (__  |__  ) / / /
|__/|__/\___/_.___/____/____/_/ /_/     

Now started ...''')

@itchat.msg_register([itchat.content.TEXT])
def simple_reply(msg):
    if msg['Type'] == TEXT:
    	output=""
    	try:
	    	if msg['Content'].startswith('__ssh__'):
	    		print("local-ssh-connection")
	    		output="local-ssh-connection"
	    	elif msg['Content']=='hand':
	    		status=0
	    		output='welcome '+msg['FromUserName']
        except Exception,e:
			itchat.send(u'.error ,%s , %s' % (repr(e),output), msg['FromUserName'])
			return ""
	if len(output) > 16000:
		output = u'response unreachable!'
    itchat.send(u'%s' % output, msg['FromUserName'])

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	welcome()
	itchat.auto_login(enableCmdQR=2, hotReload=True)
	itchat.run()


