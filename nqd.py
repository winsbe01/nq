#!/usr/bin/env python3

import socket
import spotipy
import spotipy.util as sutil
import configparser
from mpg123 import Mpg123, Out123
from threading import Thread
from time import sleep, time
from pathlib import Path

class Player:

    def __init__(self, loc):
        self.loc = loc
        self.paused = False
        self.stopped = False

    def toggle(self):
        yield

    def stop(self):
        yield

    def play(self):
        yield

class LocalPlayer(Player):

    def __init__(self, loc):
        super().__init__(loc)

    def toggle(self):
        self.paused = not self.paused

    def stop(self):
        self.stopped = True

    def play(self):
        mp3 = Mpg123(self.loc)
        out = Out123()
        frames = mp3.iter_frames(out.start)
        while True:
            if self.stopped:
                break
            elif not self.paused:
                try:
                    out.play(next(frames))
                except StopIteration:
                    break
            else:
                sleep(0.5)

class SpotifyPlayer(Player):

    def __init__(self, loc, sp, dev):
        super().__init__(loc)
        self.sp = sp
        self.sp.transfer_playback(dev, force_play=False)

    def toggle(self):
        if self.paused:
            self.sp.start_playback()
            self.paused = False
        else:
            self.sp.pause_playback()
            self.paused = True

    def stop(self):
        self.stopped = True

    def get_cur_ms(self):
        return int(round(time() * 1000))

    def play(self):
        i = [self.loc]
        self.sp.start_playback(uris=i)

        cur_ms = self.get_cur_ms()
        song_ms = self.sp.currently_playing()['item']['duration_ms']
        target_ms = cur_ms + song_ms

        while True:
            if self.stopped:
                self.sp.next_track()
                break
            elif target_ms < self.get_cur_ms():
                break
            else:
                sleep(0.5)


class PlayerManager:
    
    def __init__(self):
        self.read_config()
        self.spotipy = self.spotify_authorize()

    def write_queue(self, queue):
        with open(self.queuefile, 'w') as fil:
            fil.writelines(queue)

    def get_queue(self):
        with open(self.queuefile, 'r') as fil:
            lines = fil.readlines()
        if not lines:
            return None
        ret = lines.pop(0).strip('\n').split(maxsplit=1)
        return ret, lines

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(Path("~/.config/nq/server.config").expanduser())

        # get spotify stuff
        self.spotify_username = config['spotify']['username']
        self.spotify_client_id = config['spotify']['client_id']
        self.spotify_client_secret = config['spotify']['client_secret']
        self.spotify_device = config['spotify']['device']

        # get general stuff
        self.queuefile = Path(config['general']['queuefile']).expanduser()

        self.spotify_scopes = 'user-library-read user-read-currently-playing user-modify-playback-state'
        self.spotify_redirect_url = 'https://localhost'

    def spotify_authorize(self):

        # try and get a token
        token = sutil.prompt_for_user_token(
                self.spotify_username,
                self.spotify_scopes,
                self.spotify_client_id,
                self.spotify_client_secret,
                self.spotify_redirect_url)

        # if we get one, return a spotify object
        if token:
            return spotipy.Spotify(auth=token)
        else:
            return None

    def toggle(self):
        self.player.toggle()        

    def next(self):
        self.player.stop()

    def run(self):
        next_track, queue = self.get_queue()
        while next_track != None:
            #next_track = self.pop_queue()
            # write queue
            self.write_queue(queue)
            print(next_track)
            if next_track is not None:
                if next_track[0] == "LOCAL":
                    self.player = LocalPlayer(next_track[1])
                elif next_track[0] == "SPOTIFY":
                    self.player = SpotifyPlayer(next_track[1], self.spotipy, self.spotify_device)
                else:
                    raise Exception("bad track type!")
                p = Thread(target=self.player.play())
                p.start()
                p.join()

                # get next song
                next_track, queue = self.get_queue()
            else:
                break


if __name__ == "__main__":
    HOST = ''
    PORT = 55555
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        pm = PlayerManager()
        playing = False
        started = False
        s.bind((HOST,PORT))
        s.listen(1)
        while(True):
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                if not data:
                    break
                str_data = data.decode("utf-8").strip('\n')
                sd_split = str_data.split(' ')
                if sd_split[0] == 'play':
                    if not started and not playing:
                        Thread(target=pm.run).start()
                        playing = True
                        started = True
                elif sd_split[0] == 'toggle':
                    if started:
                        pm.toggle()
                elif sd_split[0] == 'next':
                    if started:
                        pm.next()
                else:
                    conn.sendall(b"unknown: " + data)
