# some functions for musicbot
import requests
import json

from player import Player


player = Player()


def get_real_url_from_id(id):
    '''
        Get the real url from the song id of Netease Cloud Music
        song id is 108297 in https://music.163.com/#/song?id=108297
        real url is like https://m10.music.126.net/20180807231744/121e287fe9deaf176e48518ceaddb314/ymusic/d951/6a2f/ac6f/7128783d489dcdb637b5ac218d3b79cf.mp3
    '''

    url = f'https://api.imjad.cn/cloudmusic/?type=song&id={id}'
    r = requests.get(url)
    r_dict = json.loads(r.text)
    if r_dict['data'][0]['code'] == 404:
        print(f'Incorrect song id: {id}')

    return r_dict['data'][0]['url']


def get_detail_from_id(id):
    '''
        Get song name and artist
    '''

    url = f'https://api.imjad.cn/cloudmusic/?type=detail&id={id}'
    r = requests.get(url)
    r_dict = json.loads(r.text)
    if not r_dict['songs']:
        print(f'Incorrect song id: {id}')
        return None, None
    name, artist = r_dict['songs'][0]['name'], r_dict['songs'][0]['ar'][0]['name']

    return name, artist


def search_songs(key, limit=5, page=1):
    '''
        Search songs by keyword
    '''
    url = f'https://music-api-jwzcyzizya.now.sh/api/search/song/netease?key={key}&limit={limit}&page={page}'
    r = requests.get(url)
    r_dict = json.loads(r.text)
    if r_dict['success'] == True:
        return [{
            'name': item['name'],
            'id': item['id'],
            'artist': item['artists'][0]['name']
        } for item in r_dict['songList']]


def play_by_id(id):
    url = get_real_url_from_id(id)
    if not url:
        return 'Incorrect id or song has been removed'

    name, artist = get_detail_from_id(id)
    player.set_player(url)
    player.play()
    return f':musical_note: {name}-{artist}'

def play_by_key(key):
    song_list = search_songs(key)
    for song in song_list:
        url = get_real_url_from_id(song['id'])
        if not url:
            continue
        return play_by_id(song['id'])
    return 'Not found'

def replay():
    player.play()
    return 'Music is play now'


def pause():
    player.pause()
    return 'Music is pause now'


def stop():
    player.stop()
    return 'Music is stop now'

def help():
    help_text = '''
Welcome!
You can use the following command to operate the musicbot:
1. play {key} # search song by keyword and play it
2. play id {id} # id is 108297 in `https://music.163.com/#/song?id=108297`
3. replay # continue play song after pause it
4. pause
5. stop
6. help
'''
    return help_text
