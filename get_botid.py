import os
import sys

from slackclient import SlackClient

BOT_NAME = 'musicbot'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

if __name__ == '__main__':

    api_call = slack_client.api_call('users.list')
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print(f'Bot ID for {user["name"]} is {user.get("id")}')
    else:
        print(f'could not find bot user with the name {BOT_NAME}')
