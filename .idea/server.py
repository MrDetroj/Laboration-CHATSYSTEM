from base import *
from config import *
import socket, threading, time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(QUEUE_SIZE)
s.settimeout(TIMEOUT)
state = ThreadState()

channels = {'SYSAR': [], 'DISKOFIL': []}
users = {}

# TODO_: part 1
class User:
    def __init__(self, uid, sock):
        self.id = uid
        self.socket = sock
        self.queue = []
        self.connected = True


# TODO_: part 1 & 2
def client_handle(c_sock, c_addr, state):  # to be implemented
    c_sock.settimeout(TIMEOUT)

    # Read the first message from the client # and use this as the nickname/username

    nick = read_buf(c_sock)
    user = User(nick, c_sock)
    users[nick] = user
    print('ALERT::User {} at {}'.format(nick, c_addr))

    # for nick in channels['SYSAR']:
    # for _usr in channels['SYSAR']:
    users[nick].queue.append(('SERVER', nick + ' has joined'))
        # send_buf(users[_usr].socket, 'SERVER', nick + ' has joined')


    channels['SYSAR'].append((nick))
    # users[nick].queue.append((nick, msg))

    print('Choose channel(s):')
    for key, value in channels.items():
        users[nick].queue.append(('SERVER', key))


    print(channels)
    while state.running and nick in users:
        # Read next message from client
        msg = read_buf(c_sock)

        # If msg is empty, try again
        if not msg:
            continue

        # First word in message is the receiver
        # Remaining words are message to send
        msg = msg.split(' ')
        receiver, msg = msg[0], ' '.join(msg[1:])

        # Put message on receiver queue if receiver # is connected
        
        # if receiver in users:
        users[nick].queue.append((user.id, msg))
    c_sock.close()


# TODO_: part 2.1
def client_send(state):
    """Send all unsent messages with a delay of 0.05 seconds"""
    while state.running:
        disconnected_users = []
        time.sleep(0.05)
        for nick in users:
            nick, queue = nick, users[nick].queue
            while len(queue) > 0:
                sender, msg = queue.pop(0)
                message = '{}> {}'.format(sender, msg)
                print(message)
                try:
                    for _usr in channels['SYSAR']:
                        # if _usr != sender:
                        print('should send')
                        send_buf(users[_usr].socket, message)
                except:
                    if nick not in disconnected_users:
                        disconnected_users.append(nick)
        for nick in disconnected_users:
            print('ALERT::{} disconnected'.format(nick))
            del users[nick]



# TODO_: part 2.2
def ping_thread(state):
    """Send PING message to users every PING_FREQ seconds"""
    while state.running:
        time.sleep(PING_FREQ)
        # for nick in users:
            # users[nick].queue.append(('SERVER', 'PING'))


def input_thread(state):
    stop = input("Server started, press Enter top stop.\n")
    state.running = False


# TODO_: part 3
t_input = threading.Thread(target=input_thread, args=(state,))
t_send = threading.Thread(target=client_send, args=(state,))
t_ping = threading.Thread(target=ping_thread, args=(state,))

t_ping.start()
t_send.start()
t_input.start()


# TODO_: part 3
client_threads = []
while state.running:
    try:
        c_sock, c_addr = s.accept()
        c_thread = threading.Thread(target=client_handle, args=(c_sock, c_addr, state))
        client_threads.append((c_thread, c_addr))
        c_thread.start()
    except:
        pass


# TODO: part 4
print("Exiting, waiting for threads")

t_input.join()
print("Input thread stopped")

t_send.join()
print("Send thread stopped")

t_ping.join()
print("Ping thread stopped")

for t, addr in client_threads:
    t.join()
    print("Thread for address {} stopped".format(addr))
print("Client threads stopped")

s.close()
print("Socket closed")
