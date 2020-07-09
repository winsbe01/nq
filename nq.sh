
all_ids="$HOME/.config/nq/*.ids"
all_tracks="$HOME/.config/nq/*.tracks"
queue="$HOME/.config/nq/queue"

play() {
    echo "play" | nc localhost 55555
}

pause() {
    echo "pause" | nc localhost 55555
}

toggle() {
    echo "toggle" | nc localhost 55555
}

next() {
    echo "next" | nc localhost 55555
}

add() {
    while read line; do
        grep -h "^`echo $line | cut -d ' ' -f 1`" $all_ids >> $queue
    done
}

refresh() {
	case "$1" in
		spotify)
			echo "spotify_refresh" | nc localhost 55555
			;;
		local)
			echo "local_refresh" | nc localhost 55555
			;;
		*)
			echo "unknown library: $1"
			;;
	esac
			
}

stat() {
    song_id=`echo "status" | nc localhost 55555`
	grep -h $song_id $all_tracks | print_track
}

playlist() {
	while read line; do
		grep -h `echo $line | cut -d ';' -f 1` $all_tracks | print_track
	done < $queue
}

print_track() {
    awk -F';;' '{ print substr($1,1,8) "  " $4 "/" $3 "/" $5 " - " $6 }'
}

search() {
    if [[ -z "$2" ]]; then
        printf %s\\n "missing a search term!"
	return 1
    fi
    case "$1" in
        artist)
    	    artist_list=`cat $all_tracks | awk -F';;' '{ print ";;" $4 ";;" }' | sort | uniq | grep -i "$2"`
            IFS=$'\n'
            for artist in $artist_list; do
                grep -h "$artist" $all_tracks | print_track | sort -k 2
            done
			unset IFS
	    ;;
        album)
    	    album_list=`cat $all_tracks | awk -F';;' '{ print ";;" $3 ";;" }' | sort | uniq | grep -i "$2"`
            IFS=$'\n'
            for album in $album_list; do
                grep -h "$album" $all_tracks | print_track | sort -k 2
            done
			unset IFS
		;;
        title)
    	    title_list=`cat $all_tracks | awk -F';;' '{ print ";;" $6 }' | sort | uniq | grep -i "$2"`
            IFS=$'\n'
            for title in $title_list; do
                grep -h "$title" $all_tracks | print_track | sort -k 2
            done
			unset IFS
		;;
        *)
            printf %s\\n "not recognized"
	    ;;
    esac 
}

case "$1" in
	"")
		stat
		;;
    play)
        play
        ;;
    pause)
        pause
        ;;
    next)
        next
        ;;
    toggle)
        toggle
        ;;
	refresh)
		refresh "$2"
		;;
    search)
        search "$2" "$3"
        ;;
    add)
        add
        ;;
	playlist)
		playlist
		;;
    *)
        printf %s\\n "not recognized"
        ;;
esac
