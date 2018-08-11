# musicbot

Play music from Slack: Raspberry Pi + Netease Cloud Music

Welcome!
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
