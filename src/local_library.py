from pathlib import Path
import hashlib
import glob
import eyed3


class LocalLibrary:

    def __init__(self, format_string,
                        local_library_path):
        self.format_string = format_string
        self.local_library_path = local_library_path
        self.local_tracks_file = Path("~/.config/nq/local.tracks").expanduser()
        self.local_ids_file = Path("~/.config/nq/local.ids").expanduser()

        self.generate_ids_file()
        self.generate_tracks_file()

    def generate_ids_file(self):
        tracks = glob.iglob('{}/**/*.mp3'.format(self.local_library_path), recursive=True)
        with open(self.local_ids_file, 'w') as fil:
            for t in tracks:
                tid = hashlib.sha256(t.encode()).hexdigest()
                fil.write("{};;LOCAL;;{}\n".format(tid, t))

    def generate_tracks_file(self):
        with open(self.local_ids_file, 'r') as id_fil:
            with open(self.local_tracks_file, 'w') as tracks_fil:
                for l in id_fil.readlines():
                    id_record = l.strip().split(';;')
                    tag = eyed3.load(id_record[2]).tag
                    if tag:
                        tracks_fil.write(self.format_string.format(id_record[0],
                                        tag.artist,
                                        tag.album,
                                        tag.album_artist,
                                        str(tag.track_num[0]).zfill(2),
                                        tag.title))
                    else:
                        tracks_fil.write(self.format_string.format(f,"","","","",""))
