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
                    print("analyzing: " + str(l))
                    id_record = l.strip().split(';;')
                    edo = eyed3.load(id_record[2])
                    if edo is None:
                        print("object can't load: " + str(id_record[2]))
                    else:

                        tag = edo.tag
                        seconds = int(edo.info.time_secs)

                        if tag:

                            if tag.album_artist not in ("", None):
                                artist = tag.album_artist
                            else:
                                artist = tag.artist

                            tracks_fil.write(self.format_string.format(id_record[0],
                                        artist,
                                        tag.album,
                                        str(tag.track_num[0]).zfill(2),
                                        tag.title,
                                        seconds))
                        else:
                            print("no tag!")
                            #tracks_fil.write(self.format_string.format(id_record[0],"","","","",""))
