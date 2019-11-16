from websocket_server import WebsocketServer
import binascii
import time
sample = {
    'roomid' : 0,
    'p1': {},
    'p2':{}    
}
room = []
# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    # server.send_message_to_all("Hey all, a new client has joined us")
    server.send_message(client,"welcom~")



# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + '..'
        
    for p in range(0,len(room)):
        # print(room[p]['roomid'])
            if ((room[p]['p1']) == client):
                key = p
                server.send_message(room[key]['p2'], "somebody:"+message)
                break
            if ((room[p]['p2']) == client):
                key = p
                server.send_message(room[key]['p1'], "somebody:"+message)
                break

    print("Client(%d) said: %s" % (client['id'], message))
    if (message == "/room"):
        tmp_sample = sample
        tmp_sample['p1'] = client
        now_time=str(time.time())
        tmp_sample['roomid']=binascii.crc32(str.encode(now_time))
        room.append(tmp_sample) 
        server.send_message(client,"creat room success: \n"+str(tmp_sample['roomid']))
        
        print("room:", room)
    exp_input=""
    try:
        if(message[:5]=="/room"):
            exp_input = message.split('=')[1]
            # print(exp_input)
            for p in range(0,len(room)):
                print(room[p]['roomid'])
                if (str(room[p]['roomid']) == exp_input):
                    key = p
                    
                    room[p]['p2']=client
                    # print(p)
                    
                    server.send_message(room[key]['p1'], "success join room")
                    server.send_message(room[key]['p2'], "success join room")
                    
                    break
                    
        if (message == '/all'):
            print(room)

    except:
        pass
    
    # server.send_message_to_all("Client(%d) said: %s" % (client['id'], message))
    # server.send_message(client,"Client(%d) said: %s" % (client['id'], message))


PORT=9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()



'''
{
 "action":"guess",
 "user_guess":"1234"
 
}

{
 "action":"send_message,
 "send_message":"message"
}
{
 "action":"respond_guess",
 "respond_guess":"1A1B"
 
}
{
 "action":"recv_message",
 "recv_message":"message"
}
'''