import os
import time
from slackclient import SlackClient

import functions
from player import Player

BOT_ID = os.environ.get('BOT_ID')

AT_BOT = '<@' + BOT_ID + '>'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel, player):
    '''
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    '''

    response = ''

    if command.startswith('play id '):
        response = player.play_by_id(command[7:].strip())
    elif command.startswith('play '):
        response = player.play_by_key(command[4:].strip())
    elif command.startswith('add id '):
        response = player.add_by_id(command[6:].strip())
    elif command.startswith('add '):
        response = player.add_by_key(command[3:].strip())
    elif command == 'next':
        response = player.next()
    elif command == 'list':
        response = player.show_list()
    elif command == 'random':
        response = player.random()
    elif command == 'current':
        response = player.current()
    elif command == 'clear':
        response = player.clear()
    elif command == 'replay':
        response = player.play()
    elif command == 'pause':
        response = player.pause()
    elif command == 'stop':
        response = player.stop()
    elif command == 'help':
        response = functions.help()

    if response:
        slack_client.api_call(
            'chat.postMessage', channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    '''
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    '''
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == '__main__':
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print('MusicBot connected and running!')
        player = Player()
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, player)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print('Connection failed. Invalid Slack token or bot ID')
