# some functions for musicbot
import requests
import json


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
    name, artist = r_dict['songs'][0]['name'], r_dict['songs'][0]['ar'][0][
        'name']

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


def help():
    help_text = '''
*Welcome to shoppo music station!*
You can use the following command to operate the musicbot:

1. *play* {_key_}
    search for songs by keyword and play
2. *play id* {_id_}
    id is like `108297` in `https://music.163.com/#/song?id=108297`
3. *add* {_key_}
    search for songs by keyword and add to playlist
4. *add id* {_id_}
    similar to the second item
5. *next*
    play the next song of the playlist
6. *list*
    display the song list, if the list length exceeds 10, the first 10 are displayed
7. *random*
    shuffle a song
8. *current*
    display the currently playing song information
9. *clear*
    stop music and clear playlist
10. *replay*
    replay the paused song
11. *pause*
    pause the current song
12. *stop*
    stop the current song
13. *help*
    show help infomation
'''
    return help_text
