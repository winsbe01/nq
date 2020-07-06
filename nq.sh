
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
        grep "^`echo $line | cut -d ' ' -f 1`" $all_ids | awk -F';;' '{ print $2 " " $3 }' >> $queue
    done
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
                grep "$artist" $all_tracks | awk -F';;' '{ print substr($1,1,8) "  " $4 "/" $3 "/" $5 " - " $6 }' | sort -k 2
            done
			unset IFS
	    ;;
        album)
    	    album_list=`cat $all_tracks | awk -F';;' '{ print ";;" $3 ";;" }' | sort | uniq | grep -i "$2"`
            IFS=$'\n'
            for album in $album_list; do
                grep "$album" $all_tracks | awk -F';;' '{ print substr($1,1,8) "  " $4 "/" $3 "/" $5 " - " $6 }' | sort -k 2
            done
			unset IFS
		;;
        title)
    	    title_list=`cat $all_tracks | awk -F';;' '{ print ";;" $6 }' | sort | uniq | grep -i "$2"`
            IFS=$'\n'
            for title in $title_list; do
                grep "$title" $all_tracks | awk -F';;' '{ print substr($1,1,8) "  " $4 "/" $3 "/" $5 " - " $6 }' | sort -k 2
            done
			unset IFS
		;;
        *)
            printf %s\\n "not recognized"
	    ;;
    esac 
}

case "$1" in
    play)
        play
        ;;
    next)
        next
        ;;
    toggle)
        toggle
        ;;
    search)
        search "$2" "$3"
        ;;
    add)
        add
        ;;
    *)
        printf %s\\n "not recognized"
        ;;
esac
