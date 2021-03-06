from base import *
from config import *
import socket, threading, time


def send_thread(s, send_to, msg, state):
    i = 0
    while state.running:
        i += 1
        try:
            message = '{} {} ({})'.format(send_to, msg, i)
            send_buf(s, message)
            return
        except:
            print("Lost connection to server.")
            state.running = False
        time.sleep(5)


def recv_thread(s, state):
    while state.running:
        msg = read_buf(s)
        if msg:
            print('\n', msg)


def run_client(nickname, send_to, msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    s.connect((HOST, PORT))
    send_buf(s, nickname)

    state = ThreadState()
    t1 = threading.Thread(target=send_thread, args=(s, send_to, msg, state))
    t2 = threading.Thread(target=recv_thread, args=(s, state))
    for t in [t1, t2]:
        t.start()

    while True:
        # receiver = input('type receiver: ')
        message = input('')
        
        send_thread(s, receiver, message, state)

    # state.running = False
    # stop = input("Press Enter to quit.\n")
    # state.running = False

    print('Exiting, waiting for threads')
    t1.join()
    print('Send thread stopped')
    t2.join()
    print('Receive thread stopped')
    s.close()
    print('Socket closed')


if __name__ == '__main__':
    import sys

    # if len(sys.argv) < 4:
    #     print('Must supply nickname, receiver and message!')
    # else:
    #     nick, receiver, msg = sys.argv[1], sys.argv[2], ' '.join(sys.argv[3:])
    #
    #     print('Nickname: {}'.format(nick))
    #     print('Receiver: {}'.format(receiver))
    #     print('Message: {}'.format(msg))


    nick = input('Enter nick: ')
    receiver = input('Enter receiver: ')
    msg = ''

    run_client(nick, receiver, msg)
