import socket
import sys
from emoji import demojize
import configparser
import parser

config_obj = configparser.ConfigParser()
config_obj.read("config.ini")
userinfo = config_obj["user_info"]

server = 'irc.chat.twitch.tv'
port = 6667
nickname = userinfo["nickname"]
token = 'oauth:' + userinfo["token"]
channel = '#' + userinfo["channel"]

try:
    socket = socket.socket()

    socket.connect((server, port))

    socket.send(f"PASS {token}\n".encode('utf-8'))
    socket.send(f"NICK {nickname}\n".encode('utf-8'))
    socket.send(f"JOIN {channel}\n".encode('utf-8'))

    comment = ''

    file = open("chat.log", "a+")

    while True:
        response = socket.recv(2048).decode('utf-8')

        if response.startswith('PING'):
            socket.send("PONG\n".encode('utf-8'))
        elif len(response) > 0:
            file.write(demojize(response))
            if response.find('\r\n'):
                splitter = demojize(response).split('\r\n')
                comment = comment + splitter[0]
                parser.get_chat(comment)
                i = 1
                while i < len(splitter) - 1:
                    comment = splitter[i]
                    parser.get_chat(comment)
                    i = i + 1
                comment = splitter[i]

except KeyboardInterrupt:
    try:
        socket.close(0)
        file.close()
        sys.exit(0)
    except Exception:
        sys.exit(0)