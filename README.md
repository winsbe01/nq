# nq
a scrappy music player for mp3s and Spotify

## goals
- *simple* -> support only the features I want/need, which is a tiny subset of most music players
- *unix-y* -> libraries are just text files, commands support UNIX pipeline, controller is POSIX
- *server/client* -> a music player need not take up a whole window all the time
- *minimal requirements* -> don't make me download half the internet
- *fast* -> commands should be nearly instantaneous

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
coming soon

## setup
coming soon

## TODO
- volume discrepancy between local/Spotify (this might be a mac/portaudio issue)
- Spotify craps out when it hasn't heard from the API in awhile
- fix Spotify pause issue
- commands for status and current queue
- more id3 tags (year? track length?)
