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
def genQ():
    ans=''
    while 1:
    if (len(ans) == 4):
        break
    inp = random.choice('0123456789')
    if inp not in ans:
        ans+=inp
    return (ans)
def chk_ans(guess,ans):
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
# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    # server.send_message_to_all("Hey all, a new client has joined us")
    resend = sample_json
    resend['recv_message']="welcome"
    server.send_message(client,json.dumps(resend))



# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + '..'
    try:
        message_djson = json.loads(message)
        
        if (message_djson['action'] == 'user_guess'):
            resend = sample_json
            resend['action'] = 'respond_guess'
            for key in range(0,len(room)):
                if ((room[key]['p1']) == client or (room[key]['p2']) == client):
                    ret = chk_ans(message_djson['user_guess'], room[key]['ans'])
                    if (ret == 'win'):
                        resend['respond_guess']='win'
                        server.send_message(client, json.dumps(resend))
                        
                    else:
                        resend['respond_guess']=ret
                        server.send_message(client, json.dumps(resend))
                    break
               
        if (message_djson['action'] == 'send_message' ):
            # room chat    
            resend = sample_json
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
            tmp_sample = sample
            tmp_sample['p1'] = client
            now_time=str(time.time())
            tmp_sample['roomid']=binascii.crc32(str.encode(now_time))
            room.append(tmp_sample)
            resend = sample_json
            resend['action'] = 'creat_room'
            resend['creat_room']=tmp_sample['roomid']
            server.send_message(client,json.dumps(resend))
        if (message_djson['action'] == 'join_room'):
            for p in range(0,len(room)):
                print(room[p]['roomid'])
                if (str(room[p]['roomid']) == message_djson['join_room']):
                    key = p
                    
                    room[p]['p2']=client
                    # print(p)
                    resend = sample_json
                    resend['action'] = 'respond_message'
                    resend['respond_message'] = 'success join room'
                    room[key]['ans']=genQ()
                    server.send_message(room[key]['p1'],json.dumps(resend))
                    server.send_message(room[key]['p2'],json.dumps(resend))
                    
                    break
            
        
            
        

    

    # print("Client(%d) said: %s" % (client['id'], message))
    


    
    # server.send_message_to_all("Client(%d) said: %s" % (client['id'], message))
    # server.send_message(client,"Client(%d) said: %s" % (client['id'], message))


PORT=9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()



