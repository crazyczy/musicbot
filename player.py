import vlc
import random

import functions


class Player:
    '''
        Some functions to control player
    '''

    def __init__(self):
        '''
            init player
        '''
        self.songlist = []
        self.instance = vlc.Instance()
        self.init_player()

    def init_player(self):
        self.player = self.instance.media_player_new()
        self.events = self.player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached,
                                 self.song_finished)

        self.current_name = None
        self.current_artist = None

    def set_player(self, url):
        media = self.instance.media_new(url)
        self.player.set_media(media)

    def play(self):
        self.player.play()
        if self.current_name and self.current_artist:
            return f':musical_note: {self.current_name}-{self.current_artist}'
        return 'Music is play now'

    def pause(self):
        self.player.pause()
        if self.current_name and self.current_artist:
            return f':musical_note: {self.current_name}-{self.current_artist} is pause now'
        return 'Music is pause now'

    def stop(self):
        self.player.stop()

        if self.current_name and self.current_artist:
            return f':musical_note: {self.current_name}-{self.current_artist} has stopped'

        self.current_name = None
        self.current_artist = None
        return 'Music has stopped'

    def show_list(self):
        length = len(self.songlist)
        if not length:
            return 'Song list is empty now'

        text = 'Song List is more than 10 songs, show the top 10:\n' if length > 10 else ''
        for i in range(0, min(10, length)):
            text += f'{i+1}. {self.songlist[i]["name"]}-{self.songlist[i]["artist"]}\n'

        return text

    def next(self):
        length = len(self.songlist)
        if length <= 1:
            self.songlist = []
            self.player.stop()
            return 'Song list is empty now, please add new song'
        else:
            self.songlist = self.songlist[1:]
            song = self.songlist[0]
            self.play_by_id(song['id'], song['name'], song['artist'])

    def song_finished(self, event):
        self.init_player()
        self.next()

    def current(self):
        if self.current_name and self.current_artist:
            return f':musical_note: {self.current_name}-{self.current_artist}'
        else:
            return 'No song is play now'

    def clear(self):
        self.player.stop()
        self.songlist = []
        return 'Song list is empty now'

    def random(self):
        while True:
            id = random.randint(10000, 1000000)
            url = functions.get_real_url_from_id(id)
            if not url:
                continue
            return self.play_by_id(id)

    def play_by_id(self, id, name=None, artist=None):
        url = functions.get_real_url_from_id(id)
        if not url:
            return 'Incorrect id or song has been removed'
        if not name or not artist:
            name, artist = functions.get_detail_from_id(id)

        self.set_player(url)
        self.player.play()
        self.current_name = name
        self.current_artist = artist
        return f':musical_note: {name}-{artist}'

    def play_by_key(self, key):
        song_list = functions.search_songs(key)
        if song_list:
            for song in song_list:
                url = functions.get_real_url_from_id(song['id'])
                if not url:
                    continue
                return self.play_by_id(song['id'], song['name'],
                                       song['artist'])
        return 'Not found'

    def add_by_id(self, id, name=None, artist=None):
        url = functions.get_real_url_from_id(id)
        if not url:
            return 'Incorrect id or song has been removed'
        if not name or not artist:
            name, artist = functions.get_detail_from_id(id)

        self.songlist.append({
            'id': id,
            'name': name,
            'artist': artist,
        })
        if len(self.songlist) == 1:
            return self.play_by_id(id, name, artist)

        return f'add success {name}-{artist}'

    def add_by_key(self, key):
        song_list = functions.search_songs(key)
        if song_list:
            for song in song_list:
                url = functions.get_real_url_from_id(song['id'])
                if not url:
                    continue
                self.songlist.append({
                    'id': song['id'],
                    'name': song['name'],
                    'artist': song['artist'],
                })
                if len(self.songlist) == 1:
                    return self.play_by_id(song['id'], song['name'],
                                           song['artist'])

                return f'add success {song["name"]}-{song["artist"]}'
        return f'Not found for {key}'
