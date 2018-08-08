import vlc


class Player:
    '''
        Some functions to control player
    '''

    def __init__(self):
        '''
            init player
        '''
        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player = self.instance.media_player_new()

    def set_player(self, url):
        media = self.instance.media_new(url)
        self.player.set_media(media)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()
