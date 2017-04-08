
# A simple Evernote API demo script that lists all notebooks in the user's
# account and creates a simple test note in the default notebook.
#
# Before running this sample, you must fill in your Evernote developer token.
#
# To run (Unix):
#   export PYTHONPATH=../../lib; python EDAMTest.py
#

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient
import time,datetime
from views import yc

hq,lq,strrq,xqqh=yc()[0],yc()[1],yc()[2],yc()[3]+1

rq=datetime.datetime.strptime(strrq,"%Y-%m-%d") #转换为datetime.datetime格式 方便计算相加时间
tmrq=datetime.datetime.strptime(strrq, "%Y-%m-%d" ).timetuple() #字符串转time 获取星期
xq=time.strftime('%w',tmrq)#0-6,0为周日
#下期开奖日期
def xqrq(xq):
    if xq == '0' or xq == '2' or xq=='5':
        f=rq + datetime.timedelta(days=2) #下周二，本周四日期
    if xq =='1' or xq =='3':
        f=rq + datetime.timedelta(days=1) #本周日日期
    if xq =='4':
        f=rq + datetime.timedelta(days=3)
    return f.strftime('%Y%m%d')

# Real applications authenticate with Evernote using OAuth, but for the
# purpose of exploring the API, you can get a developer token that allows
# you to access your own Evernote account. To get a developer token, visit
# https://sandbox.evernote.com/api/DeveloperToken.action
auth_token = "abasddfasdfawea"

if auth_token == "your developer token":
    print("Please fill in your developer token")
    print("To get a developer token, visit " \
          "https://sandbox.evernote.com/api/DeveloperToken.action")
    exit(1)

# Initial development is performed on our sandbox server. To use the production
# service, change sandbox=False and replace your
# developer token above with a token from
# https://www.evernote.com/api/DeveloperToken.action
client = EvernoteClient(token=auth_token, service_host='app.yinxiang.com') #

user_store = client.get_user_store()

version_ok = user_store.checkVersion(
    "Evernote EDAMTest (Python)",
    UserStoreConstants.EDAM_VERSION_MAJOR,
    UserStoreConstants.EDAM_VERSION_MINOR
)
print("Is my Evernote API version up to date? ", str(version_ok))
print("")
if not version_ok:
    exit(1)

note_store = client.get_note_store()

# List all of the notebooks in the user's account
notebooks = note_store.listNotebooks()
print("Found ", len(notebooks), " notebooks:")
for notebook in notebooks:
    print("  * ", notebook.name,notebook.guid)

print()
print("Creating a new note in the 双色球 notebook")
print()
# To create a new note, simply create a new Note object and fill in
# attributes such as the note's title.
note = Types.Note()
note.title =xqrq(xq)+' '+str(xqqh)+' 期双色球PYTHON预测'

# To include an attachment such as an image in a note, first create a Resource
# for the attachment. At a minimum, the Resource contains the binary attachment
# data, an MD5 hash of the binary data, and the attachment MIME type.
# It can also include attributes such as filename and location.
#image = open('enlogo.png', 'rb').read()
#md5 = hashlib.md5()
#md5.update(image)
#hash = md5.digest()

#data = Types.Data()
#data.size = len(image)
#data.bodyHash = hash
#data.body = image

#resource = Types.Resource()
#resource.mime = 'image/png'
#resource.data = data

# Now, add the new Resource to the note's list of resources
#note.resources = [resource]

# To display the Resource as part of the note's content, include an <en-media>
# tag in the note's ENML content. The en-media tag identifies the corresponding
# Resource using the MD5 hash.
#hash_hex = binascii.hexlify(hash)
#hash_str = hash_hex.decode("UTF-8")

# The content of an Evernote note is represented using Evernote Markup Language
# (ENML). The full ENML specification can be found in the Evernote API Overview
# at http://dev.evernote.com/documentation/cloud/chapters/ENML.php

#bz="'h'开头代表红球，'l'开头代表篮球，括号内的数字为概率"
note.content = '<?xml version="1.0" encoding="UTF-8"?>'
note.content += '<!DOCTYPE en-note SYSTEM ' \
                '"http://xml.evernote.com/pub/enml2.dtd">'
note.content += '<en-note>{} {}<br/>{} {}<br/>{} {}<br/>{}<br/>{}<br/>{}<br/>{}<br/>{}<br/>{}<br/>'.format(hq[0],lq[0],hq[1],lq[1],hq[2],lq[2],hq[3],hq[4],hq[5],hq[6],hq[7],bz)
#note.content += '<en-media type="image/png" hash="{}"/>'.format(hash_str)
note.content += '</en-note>'
note.notebookGuid='guid' #制定在双色球笔记本中创建笔记，51行获得
# Finally, send the new note to Evernote using the createNote method
# The new Note object that is returned will contain server-generated
# attributes such as the new note's unique GUID.
created_note = note_store.createNote(note)

print("Successfully created a new note with GUID: ", created_note.guid)
