import pandas as pd
import re


def get_chat(stream):
    data = []

    try:

        username, channel, message = re.search(
            ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', stream
        ).groups()

        d = {
            'channel': channel,
            'username': username,
            'message': message
        }

        #print(f'Channel: ' + channel + ' # Username: ' + username + ' # Message: ' + message)

        data.append(d)

        return d

    except Exception:
        pass

    return data