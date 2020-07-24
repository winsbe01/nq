# nq
a scrappy music player for mp3s and Spotify

## goals
- **simple** -> support only the features I want/need, which is a tiny subset of most music players
- **unix-y** -> libraries are just text files, commands support UNIX pipeline, controller is POSIX
- **server/client** -> a music player need not take up a whole window all the time
- **minimal requirements** -> don't make me download half the internet
- **fast** -> commands should be nearly instantaneous

## isn't this just mpd/mpc?
mpc is great, and was an inspiration for much of the commands. It doesn't integrate with
Spotify, though, and I want to be able to play both mp3s and Spotify tracks, back to back,
on the same playlist.

## requirements
- Python3 (yes, I know I said "fast" above)
- [mpg123](http://mpg123.org/), for playing mp3s
- a Spotify Premium account
- a Spotify player -- either the full player (ew) or [spotifyd](https://github.com/Spotifyd/spotifyd)

## install
(eventually, this will be a Makefile)
- install the requirements using pip
- copy *server.config* into ~/.config/nq/
- create an app on [your Spotify dashboard](https://developer.spotify.com/dashboard/)
- populate the client info into the *server.config*
- start *src/nqd.py*. on your first run, you will be prompted to log in to Spotify. this will be the server, you can fork this to bg.
- use the *nq.sh* script to control the player

## usage
- *nq.sh refresh spotify* - populate your Spotify saved tracks
- *nq.sh refresh local* - populate your local library
- *nq.sh search <artist|album|title> <search term>* - search your library
- *nq.sh add* - pipe results of search into this to add to the queue
- *nq.sh <play|pause>* - play/pause the song

## TODO
- volume discrepancy between local/Spotify (this might be a mac/portaudio issue)
- manage the Spotify token properly
- get Spotify device ID
- prev?
- ~fix Spotify pause issue~
- ~commands for status and current queue~
- more id3 tags (year? track length?)
- log everything
- makefile
- ~edit the queue~
- ~add to front of queue?~
- incremental refresh
