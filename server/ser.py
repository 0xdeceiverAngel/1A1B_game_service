from websocket_server import WebsocketServer
import binascii
import time
import json
import random
'''
{
 "action":guess send_message respond_guess recv_message
 "user_guess":"",
 "send_message":"",
 "respond_guess":"",
 "recv_message":""
}
'''
sample = {
    'roomid' : 0,
    'p1': {},
    'p2': {},
    'ans':''
}
sample_json ={
 "action":"",
 "user_guess":"",
 "send_message":"",
 "respond_guess":"",
 "recv_message": "",
 "creat_room": "",
 "join_room":""
}
room = []

def genQ(): # generate question
    ans=""
    while 1:
        if (len(ans) == 4):
            break
        inp = random.choice('0123456789')
        if inp not in ans:
            ans+=inp
    return(ans)

def chk_ans(guess, ans): # check ans correct or not ,if it's not correct return _A_B
    if (len(guess) !=4):
        return 'error'
    while 1:
        if (guess == ans):
            return('win')
            break
        A = 0
        B = 0
        for i in range(4):
            if (ans[i] == guess[i]):
                A = A + 1
            if (guess[i] in ans):
                B = B + 1
        B = B - A
        return (str(A) + 'A' + str(B) + 'B')

def new_client(client, server): # if new client connected,send client "wellcom"
    print("New client connected and was given id %d" % client['id'])
    # server.send_message_to_all("Hey all, a new client has joined us")
    resend = sample_json
    resend['recv_message'] = "welcome\n"
    resend['action']='recv_message'
    server.send_message(client,json.dumps(resend))



# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + '..'
    try:

        resend = sample_json
        message_djson = json.loads(message) # json decode
        print(message_djson)

        if (message_djson['action'] == 'user_guess'):

            resend['action'] = 'respond_guess'
            for key in range(0,len(room)): 
                if ((room[key]['p1']) == client or (room[key]['p2']) == client):
                    ret = chk_ans(message_djson['user_guess'], room[key]['ans'])
                    print(room[key]['ans'])
                    if (ret == 'win'):
                        resend['respond_guess']='win'
                        server.send_message(client, json.dumps(resend))
                        resend['recv_message'] = 'ans is :' + str(room[key]['ans']+'\nAnd new game on')
                        resend['action'] = 'recv_message'

                        server.send_message(room[key]['p1'],json.dumps(resend))
                        server.send_message(room[key]['p2'],json.dumps(resend))
                        room[key]['ans']=genQ()


                    else:
                        resend['respond_guess']='you send:'+message_djson['user_guess']+'\nthat not correct:'+ret
                        server.send_message(client, json.dumps(resend))
                    break

        if (message_djson['action'] == 'send_message' ):
            # room chat
            # resend = sample_json
            resend['action'] = 'recv_message'
            resend['recv_message']=message_djson['send_message']
            for key in range(0,len(room)):
                if ((room[key]['p1']) == client):
                    server.send_message(room[key]['p2'],json.dumps(resend))
                    break
                if ((room[key]['p2']) == client):
                    server.send_message(room[key]['p1'],json.dumps(resend))
                    break
        if (message_djson['action'] == 'creat_room'):
            # print(message_djson['action'])
            tmp_sample = sample
            tmp_sample['p1'] = client
            now_time=str(time.time())
            tmp_sample['roomid']=binascii.crc32(str.encode(now_time))
            room.append(tmp_sample)

            # resend = sample_json
            resend['action'] = 'creat_room'
            resend['creat_room'] = 'your room id is :' + str(tmp_sample['roomid'])
            # print(resend)
            server.send_message(client,json.dumps(resend))
        if (message_djson['action'] == 'join_room' and message_djson['join_room']!=""):
            for p in range(0,len(room)):
                print(room[p]['roomid'])
                if (str(room[p]['roomid']) == message_djson['join_room']):
                    key = p
                    # print('find')
                    room[p]['p2']=client
                    # print(p)
                    # resend = sample_json
                    resend['action'] = 'join_room'
                    resend['join_room'] = 'success join room\n'
                    room[key]['ans'] = genQ()
                    # print(resend)
                    # print(room[key]['p1'])
                    server.send_message(room[key]['p1'],json.dumps(resend))
                    server.send_message(room[key]['p2'],json.dumps(resend))

                    break
        resend.clear()
    except:
        pass

    # print("Client(%d) said: %s" % (client['id'], message))
    # server.send_message_to_all("Client(%d) said: %s" % (client['id'], message))
    # server.send_message(client,"Client(%d) said: %s" % (client['id'], message))

PORT=9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
