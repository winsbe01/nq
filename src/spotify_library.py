from pathlib import Path
import hashlib


class SpotifyLibrary:

    def __init__(self, spotify_obj, format_string):
        self.format_string = format_string
        self.spotify_tracks_file = Path("~/.config/nq/spotify.tracks").expanduser()
        self.spotify_ids_file = Path("~/.config/nq/spotify.ids").expanduser()
        self.spotify_obj = spotify_obj

        if not self.spotify_obj:
            raise Exception

        self.all_tracks = self.get_all_saved_tracks()
        self.generate_ids_and_tracks_files()

    def get_all_saved_tracks(self):
        print("getting all Spotify tracks...")
        all_tracks = []
        tracks = self.spotify_obj.current_user_saved_tracks()
        while tracks is not None:
            for track in tracks['items']:
                all_tracks.append(track)
            tracks = self.spotify_obj.next(tracks)
        print("...done! {} tracks found".format(str(len(all_tracks))))
        return all_tracks

    def generate_ids_and_tracks_files(self):
        print("generating Spotify ids and tracks files...")
        if self.spotify_ids_file.exists():
            open(self.spotify_ids_file, 'w').close()
        if self.spotify_tracks_file.exists():
            open(self.spotify_tracks_file, 'w').close()
        for t in self.all_tracks:
            uri = t['track']['uri']
            tid = hashlib.sha256(uri.encode()).hexdigest()
            with open(self.spotify_ids_file, 'a') as fil:
                fil.write("{};;SPOTIFY;;{}\n".format(tid, uri))
            with open(self.spotify_tracks_file, 'a') as fil:
                fil.write(self.format_string.format(tid,
                        t['track']['artists'][0]['name'],
                        t['track']['album']['name'],
                        t['track']['album']['artists'][0]['name'],
                        str(t['track']['track_number']).zfill(2),
                        t['track']['name']))


