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
