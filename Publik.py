# -*- coding: utf-8 -*-

import LINETCR
from LINETCR.lib.curve.ttypes import *
from gtts import gTTS
import urllib
import urllib2
import urllib3
import requests
import wikipedia
import goslate
from bs4 import BeautifulSoup
from datetime import datetime
import time,random,sys,json,codecs,threading,glob,re,os,subprocess

cl = LINETCR.LINE()
#cl.login(qr=True)
cl.login(token='En5rSYJNcHTDgnqfUFE0.2PshkH9jZu06gbOeQKJtua.rpnUwHvcoAGAtwwcAywii7Wovkkz2a8Wih5Wumv0aN0=')
cl.loginResult()
print "=5="


helpMessage =""" Up! Public bot's command
[+]/set [Cek sider]
[+]/cek [Hasil result]
[+]/ginfo [Cek info group]
[+]/gcreator [Cek group creator]
[+]/cancelall [Membatalkan semua undangan]
[+]/mentionall [Mention member]
[+]/speed [Cek speed]
[+]/leave [Bot leave]
[+]/gift [Prank gift]
[+]/kalender [Cek kalender]
[+]/wikipedia [Cek wikipedia] 
[+]/pict group [Send pict group]
[+]/lirik [Cek lirik lagu]
[+]/music [Search music]
[+]/say [Say by voice]
[+]/image [Name]
[+]/instagram [Cek instagram]
Enjoy with me(^_^)
"""
helpMessage2 ="""Rashif's only command
[+]InviteMeTo: (gid)
[+]LG
[+]RemoveAllChat
[+]Bc:
"""

mid = cl.getProfile().mid
Creator="ue2101fb9b105a2341d4d511635a12353"
admin=["ue2101fb9b105a2341d4d511635a12353"]
owner="ue2101fb9b105a2341d4d511635a12353"

contact = cl.getProfile()
profile = cl.getProfile()
profile.displayName = contact.displayName
profile.statusMessage = contact.statusMessage
profile.pictureStatus = contact.pictureStatus

wait = {
    "LeaveRoom":True,
    "AutoJoin":True,
    "Members":0,
    "Timeline":True,
    "lang":"JP"
}
settings = {
    "simiSimi":{}
    }


def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text
    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1


def bot(op):
    try:
#--------------------END_OF_OPERATION--------------------
        if op.type == 0:
            return
#-------------------NOTIFIED_READ_MESSAGE----------------
        if op.type == 55:
	    try:
	      group_id = op.param1
	      user_id=op.param2
	      subprocess.Popen('echo "'+ user_id+'|'+str(op.createdTime)+'" >> dataSeen/%s.txt' % group_id, shell=True, stdout=subprocess.PIPE, )
	    except Exception as e:
	      print e
#------------------NOTIFIED_INVITE_INTO_ROOM-------------
        if op.type == 22:
            cl.leaveRoom(op.param1)
#--------------------INVITE_INTO_ROOM--------------------
        if op.type == 21:
            cl.leaveRoom(op.param1)

#--------------NOTIFIED_INVITE_INTO_GROUP----------------
        if op.type == 13:
            if mid in op.param3:	        
                if wait["AutoJoin"] == True:
                    cl.acceptGroupInvitation(op.param1)
                else:
		            cl.rejectGroupInvitation(op.param1)
#--------------------------SEND_MESSAGE---------------------------
        if op.type == 26:
            msg = op.message
            if msg.to in settings["simiSimi"]:
                if settings["simiSimi"][msg.to] == True:
                    if msg.text is not None:
                        text = msg.text
                        r = requests.get("http://api.ntcorp.us/chatbot/v1/?text=" + text.replace("42372956-8ac7-42bc-995b-b402ebc5fc67","+") + "&key=beta1.nt")
                        data = r.text
                        data = json.loads(data)
                        if data['status'] == 200:
                            if data['result']['result'] == 100:
                                cl.sendText(msg.to,data['result']['response'].encode('utf-8'))
        if op.type == 26:
            msg = op.message
            if msg.text in ["/ginfo"]:
                if msg.toType == 2:
                    ginfo = cl.getGroup(msg.to)
                    try:
                        gCreator = ginfo.creator.displayName
                    except:
                        gCreator = "Error"
                    if wait["lang"] == "JP":
                        if ginfo.invitee is None:
                            sinvitee = "0"
                        else:
                            sinvitee = str(len(ginfo.invitee))
                        if ginfo.preventJoinByTicket == True:
                            u = "Tertutup"
                        else:
                            u = "Terbuka"
                        cl.sendText(msg.to,"[Group name]\n" + str(ginfo.name) + "\n\n[Gid]\n" + msg.to + "\n\n[Group creator]\n" + gCreator + "\n\n[Profile status]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus + "\n\nMembers : " + str(len(ginfo.members)) + "members\n\nPending : " + sinvitee + "people\n\nQR : " + u)
                    else:
                        cl.sendText(msg.to,"[group name]\n" + str(ginfo.name) + "\n[gid]\n" + msg.to + "\n[group creator]\n" + gCreator + "\n[profile status]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus)
                else:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"Group Only")
                    else:
                        cl.sendText(msg.to,"Group Only")

#--------------------------------------------------------
            elif msg.text is None:
                return
#--------------------------------------------------------

#--------------------------------------------------------
            elif msg.text in ["/gcreator"]:
                ginfo = cl.getGroup(msg.to)
                gCreator = ginfo.creator.mid
                cl.sendText(msg.to,"Nih Group Creatornya !")                
                msg.contentType = 13
                msg.contentMetadata = {'mid': gCreator}
                cl.sendMessage(msg)
#--------------------------------------------------------
            elif msg.contentType == 16:
                if wait["Timeline"] == True:
                    msg.contentType = 0
                    msg.text = "post URL\n" + msg.contentMetadata["postEndUrl"]
                    cl.sendText(msg.to,msg.text)
#--------------------------------------------------------
            elif msg.text in ["/help"]:
                cl.sendText(msg.to,helpMessage)
            elif msg.text in ["Cek"]:
                cl.sendText(msg.to,helpMessage2)
                
#--------------------------------------------------------
            elif msg.text in ["Group list","/Glist","/glist","/botgrouplist","/BotGroupList"]:
                gid = cl.getGroupIdsJoined()
                h = ""
                jml = 0
                for i in gid:
                    gn = cl.getGroup(i).name
                    h += "\n[ * ] %s " % gn 
                    jml += 1
                cl.sendText(msg.to,"======[Daftar Group]======\n"+h+"\n\nTotal group: "+str(jml))
#--------------------------------------------------------				
            elif "InviteMeTo: " in msg.text:
              if msg.from_ in admin or owner:
                gid = msg.text.replace("InviteMeTo: ","")
                if gid == "":
                  cl.sendText(msg.to,"Invalid group id")
                else:
                  try:
                    cl.findAndAddContactsByMid(msg.from_)
                    cl.inviteIntoGroup(gid,[msg.from_])
                  except:
					cl.sendText(msg.to,"Mungkin saya tidak di dalam grup itu")
#--------------------------------------------------------				
            elif msg.text in ["LG"]:
              if msg.from_ in admin or owner:
                gid = cl.getGroupIdsJoined()
                h = ""
                for i in gid:
                  h += "[%s]:%s\n" % (cl.getGroup(i).name,i)
                cl.sendText(msg.to,h)
#--------------------------------------------------------
            elif "LeaveGroup: " in msg.text:
              if msg.from_ in admin or owner:    
				ng = msg.text.replace("LeaveGroup: ","")
				gid = cl.getGroupIdsJoined()
				for i in gid:
				    h = cl.getGroup(i).name
				    if h == ng:
				        cl.sendText(i,"Bye "+h+"~")
				        cl.leaveGroup(i)
				        cl.sendText(msg.to,"Success left ["+ h +"] group")
				    else:
						pass
#--------------------------------------------------------
            elif msg.text in ["/Left","/left","/bye","/Bye","/leave","/Leave","/BotLeave","/Botleave","/botleave"]:
                if msg.toType == 2:
                    ginfo = cl.getGroup(msg.to)
                    try:
                    	cl.sendText(msg.to,"Kakak jahat :v")
                        cl.leaveGroup(msg.to)
                    except:
                        pass
#--------------------------------------------------------
            elif msg.text in ["/cancelall"]:
                if msg.toType == 2:
                    X = cl.getGroup(msg.to)
                    if X.invitee is not None:
                        gInviMids = [contact.mid for contact in X.invitee]
                        cl.cancelGroupInvitation(msg.to, gInviMids)
                    else:
                        cl.sendText(msg.to,"Tidak ada pending member")
                else:
                    cl.sendText(msg.to,"Hanya bisa digunakan dalam grup")
#--------------------------------------------------------
            elif "/image " in msg.text:
                search = msg.text.replace("/image ","")
                url = 'https://www.google.com/search?espv=2&biw=1366&bih=667&tbm=isch&oq=kuc&aqs=mobile-gws-lite.0.0l5&q=' + search
                raw_html = (download_page(url))
                items = []
                items = items + (_images_get_all_items(raw_html))
                path = random.choice(items)
                print path
                try:
                    cl.sendImageWithURL(msg.to,path)
                    cl.sendText(msg.to,"Maaf ya kak agak slow ")
                except:
                    pass     
            elif msg.text in ["Join on","AutoJoin:on"]:
              if msg.from_ in admin or owner:
                wait["AutoJoin"] = True
                cl.sendText(msg.to,"AutoJoin already on")

            elif msg.text in ["Join off","AutoJoin:off"]:
              if msg.from_ in admin or owner:
                wait["AutoJoin"] = False
                cl.sendText(msg.to,"AutoJoin already off")
#--------------------------------------------------------
            elif msg.text in ["Simsimi on","Simisimi:on"]:
                settings["simiSimi"][msg.to] = True
                cl.sendText(msg.to," Simisimi Di Aktifkan")
                
            elif msg.text in ["Simsimi off","Simisimi:off"]:
                settings["simiSimi"][msg.to] = False
                cl.sendText(msg.to,"Simisimi Di Nonaktifkan")

#--------------------------------------------------------
#--------------------------------------------------------
            elif msg.text in ["/mentionall"]:
                group = cl.getGroup(msg.to)
                nama = [contact.mid for contact in group.members]
                cb = ""
                cb2 = "" 
                strt = int(0)
                akh = int(0)
                for md in nama:
                    akh = akh + int(6)
                    cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""
                    strt = strt + int(7)
                    akh = akh + 1
                    cb2 += "@nrik \n"
                cb = (cb[:int(len(cb)-1)])
                msg.contentType = 0
                msg.text = cb2
                msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                try:
                    cl.sendMessage(msg)
                except Exception as error:
                    print error
#--------------------------CEK SIDER------------------------------

            elif "/set" in msg.text:
                subprocess.Popen("echo '' > dataSeen/"+msg.to+".txt", shell=True, stdout=subprocess.PIPE)
                cl.sendText(msg.to, "Readpoint telah di set!")
                print "@setview"

            elif "/cek" in msg.text:
	        lurkGroup = ""
	        dataResult, timeSeen, contacts, userList, timelist, recheckData = [], [], [], [], [], []
                with open('dataSeen/'+msg.to+'.txt','r') as rr:
                    contactArr = rr.readlines()
                    for v in xrange(len(contactArr) -1,0,-1):
                        num = re.sub(r'\n', "", contactArr[v])
                        contacts.append(num)
                        pass
                    contacts = list(set(contacts))
                    for z in range(len(contacts)):
                        arg = contacts[z].split('|')
                        userList.append(arg[0])
                        timelist.append(arg[1])
                    uL = list(set(userList))
                    for ll in range(len(uL)):
                        try:
                            getIndexUser = userList.index(uL[ll])
                            timeSeen.append(time.strftime("%H:%M:%S", time.localtime(int(timelist[getIndexUser]) / 1000)))
                            recheckData.append(userList[getIndexUser])
                        except IndexError:
                            conName.append('nones')
                            pass
                    contactId = cl.getContacts(recheckData)
                    for v in range(len(recheckData)):
                        dataResult.append(contactId[v].displayName + ' ('+timeSeen[v]+')')
                        pass
                    if len(dataResult) > 0:
                        tukang = "Read By :\n*"
                        grp = '\n* '.join(str(f) for f in dataResult)
                        total = '\n\nTotal %i reader (%s)' % (len(dataResult), datetime.now().strftime('%H:%M:%S') )
                        cl.sendText(msg.to, "%s %s %s" % (tukang, grp, total))
                    else:
                        cl.sendText(msg.to, "Belum ada reader")
                    print "@viewseen"

#--------------------------------------------------------
            elif msg.text in ["RemoveAllChat"]:
              if msg.from_ in admin or owner:    
                cl.removeAllMessages(op.param2)
                cl.sendText(msg.to,"Removed all chat")
#--------------------------------------------------------
#---------------------------------------------------------
            elif '/wikipedia ' in msg.text.lower():
                  try:
                      wiki = msg.text.lower().replace("/wikipedia ","")
                      wikipedia.set_lang("id")
                      pesan="Wikipedia : "
                      pesan+=wikipedia.page(wiki).title
                      pesan+="\n\n"
                      pesan+=wikipedia.summary(wiki, sentences=1)
                      pesan+="\n"
                      pesan+=wikipedia.page(wiki).url
                      cl.sendText(msg.to, pesan)
                  except:
                          try:
                              pesan="Text Terlalu Panjang Silahkan Click link di bawah ini\n"
                              pesan+=wikipedia.page(wiki).url
                              cl.sendText(msg.to, pesan)
                          except Exception as e:
                              cl.sendText(msg.to, str(e))
            elif "Bc: " in msg.text:
                if msg.from_ in admin or owner:
		            bc = msg.text.replace("Bc: ","")
		            gid = cl.getGroupIdsJoined()
		            for i in gid:
		                cl.sendText(i,"[BROADCAST]\n\n"+bc+"\n\n#SorryBroadcast")
		            cl.sendText(msg.to,"BC Terkirim")
#--------------------------------------------------------
            #------------------------------------------------
            elif '/instagram ' in msg.text.lower():
                try:
                    instagram = msg.text.lower().replace("/instagram ","")
                    html = requests.get('https://www.instagram.com/' + instagram + '/?')
                    soup = BeautifulSoup(html.text, 'html5lib')
                    data = soup.find_all('meta', attrs={'property':'og:description'})
                    text = data[0].get('content').split()
                    data1 = soup.find_all('meta', attrs={'property':'og:image'})
                    text1 = data1[0].get('content').split()
                    user = "Nama: " + text[-2] + "\n"
                    user1 = text[-1]
                    followers = "Pengikut: " + text[0] + "\n"
                    following = "Mengikuti: " + text[2] + "\n"
                    post = "Post: " + text[4] + "\n"
                    link = "Link: " + "https://www.instagram.com/" + instagram
                    detail = "Info Akun: " + user1 + "\n\n"
                    #details = ""
                    cl.sendText(msg.to, detail + user + followers + following + post + link)
                    cl.sendImageWithURL(msg.to, text1[0])
                    #cl.sendImage(msg.to, text1[0])
                except Exception as njer:
                	cl.sendText(msg.to, str(njer))
     #-------------------------------------------------
#-----------------------------------------------
            elif "/say " in msg.text.lower():
                    query = msg.text.lower().replace("/say ","")
                    with requests.session() as s:
                        s.headers['user-agent'] = 'Mozilla/5.0'
                        url = 'https://google-translate-proxy.herokuapp.com/api/tts'
                        params = {'language': 'id', 'speed': '1', 'query': query}
                        r    = s.get(url, params=params)
                        mp3  = r.url
                        cl.sendAudioWithURL(msg.to, mp3)
#-----------------------------------------------
    #-------------------Music------------------ 
            elif '/music ' in msg.text.lower():
                try:
                    songname = msg.text.lower().replace('/music ','')
                    params = {'songname': songname}
                    r = requests.get('http://ide.fdlrcn.com/workspace/yumi-apis/joox?' + urllib.urlencode(params))
                    data = r.text
                    data = json.loads(data)
                    for song in data:
                        hasil = 'This is Your Music\n'
                        hasil += 'Judul : ' + song[0]
                        hasil += '\nDurasi : ' + song[1]
                        hasil += '\nLink Download : ' + song[4]
                        cl.sendText(msg.to, hasil)
                        cl.sendText(msg.to, "Please Wait for audio...")
                        cl.sendAudioWithURL(msg.to, song[4])
		except Exception as njer:
		        cl.sendText(msg.to, str(njer))
     #-------------------------------------------------           
            elif '/lirik ' in msg.text.lower():
                try:
                    songname = msg.text.lower().replace('/lyric ','')
                    params = {'songname': songname}
                    r = requests.get('http://ide.fdlrcn.com/workspace/yumi-apis/joox?' + urllib.urlencode(params))
                    data = r.text
                    data = json.loads(data)
                    for song in data:
                        hasil = 'Lirik Lagu : '
                        hasil += song[0]
                        hasil += '\n\n'
                        hasil += song[5]
                        cl.sendText(msg.to, hasil)
                        #cl.sendAudioWithURL(msg.to, hasil)
                except Exception as wak:
                        cl.sendText(msg.to, str(wak))
#-------------------------------------------------------------------------------------------
            elif "/pict group" in msg.text:
                group = cl.getGroup(msg.to)
                path ="http://dl.profile.line-cdn.net/" + group.pictureStatus
                cl.sendImageWithURL(msg.to, path)
#-------------------------------------------------------------------------------------------
            elif msg.text in ["/kalender"]:
	    	    wait2['setTime'][msg.to] = datetime.today().strftime('TANGGAL : %Y-%m-%d \nHARI : %A \nJAM : %H:%M:%S')
	            cl.sendText(msg.to, "KALENDER\n\n" + (wait2['setTime'][msg.to]))
            elif msg.text in ["Ê??„ÅÆ„??„?¨„?º„?≥„??","/gift"]:
                msg.contentType = 9
                msg.contentMetadata={'PRDID': 'a0768339-c2d3-4189-9653-2909e9bb6f58',
                                    'PRDTYPE': 'THEME',
                                    'MSGTPL': '5'}
                msg.text = None
                cl.sendMessage(msg)
            elif msg.text in ["/speed"]:
                start = time.time()
                print("Speed")
                elapsed_time = time.time() - start
                cl.sendText(msg.to, "Progress...")
                cl.sendText(msg.to, "%sseconds" % (elapsed_time))

#--------------------------------------------------------
        if op.type == 16:
            ginfo = cl.getGroup(op.param1) 
            cl.sendText(op.param1, "Halooo "+str(ginfo.name)+"\nTerima kasih telah mengundang saya \(^_^)/\nUntuk melihat list keyword ketik\n[/Help]Tanpa tanda kurung")
            cl.sendText(op.param1, "Jangan lupa juga add My creator: http://line.me/ti/p/mEHpAq1ejt")
#-----------------------------------------------


        if op.type == 59:
            print op


    except Exception as error:
        print error


#thread2 = threading.Thread(target=nameUpdate)
#thread2.daemon = True
#thread2.start()

while True:
    try:
        Ops = cl.fetchOps(cl.Poll.rev, 5)
    except EOFError:
        raise Exception("It might be wrong revision\n" + str(cl.Poll.rev))

    for Op in Ops:
        if (Op.type != OpType.END_OF_OPERATION):
            cl.Poll.rev = max(cl.Poll.rev, Op.revision)
            bot(Op)

