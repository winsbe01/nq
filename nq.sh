
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

addf() {
	tmpfile=$(mktemp)
	cp $queue $tmpfile
	clr
	cat | add
	cat $tmpfile | add
	rm "$tmpfile"
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

read_queue() {
	while read line; do
		grep -h `echo $line | cut -d ';' -f 1` $all_tracks | print_track
	done < $queue
}

playlist() {
	case "$1" in
		"")
			read_queue
			;;
		edit)
			tmpfile=$(mktemp)
			read_queue > $tmpfile
			"${EDITOR:-nano}" $tmpfile
			clr
			cat "$tmpfile" | add
			echo "queue updated!"
			rm "$tmpfile"
			;;
		*)
			echo "unknown playlist command: '$1'"
			;;
		esac
}

clr() {
	> $queue
}

print_track() {
    awk -F';;' '{ print substr($1,1,8) "  " $2 "/" $3 "/" $4 " - " $5 }'
}

listall() {
	cat $all_tracks | print_track | sort -k 2
}

_artist_search() {
	cat | awk -F';;' '{ print substr($1,1,8) ";;" $2 ";;" }' | grep -i "$1"
}

_album_search() {
	cat | awk -F';;' '{ print substr($1,1,8) ";;" $3 ";;" }' | grep -i "$1"
}

_title_search() {
	cat | awk -F';;' '{ print substr($1,1,8) ";;" $5 ";;" }' | grep -i "$1"
}

_inner_search() {

	# if we have no more arguments, pretty print and return
	if [[ $# -eq 0 ]]; then
		cat | print_track | sort -k 2
		return 0
	fi

	# grab the first two arguments, then shift
	typ="$1"
	term="$2"
	shift 2

	# do the search, then recurse with the rest of the arguments
	case "$typ" in
		artist)
			cat | _artist_search "$term" | cut -d ';' -f 1 | grep -h -f /dev/stdin $all_tracks | _inner_search "$@"
		;;
		album)
			cat | _album_search "$term" | cut -d ';' -f 1 | grep -h -f /dev/stdin $all_tracks | _inner_search "$@"
		;;
		title)
			cat | _title_search "$term" | cut -d ';' -f 1 | grep -h -f /dev/stdin $all_tracks | _inner_search "$@"
		;;
		*)
			printf %s\\n "not recognized: '$typ'"
		;;
	esac 
}

search() {

	

	# make sure we have an even number of arguments (not 0)
	if [ $# -eq 0 ]; then
		printf %s\\n "usage: nq search <artist|album|title> <search term> [...]"
		return 1
	elif (( $# % 2 )); then
        printf %s\\n "missing a search term!"
		return 1
    fi
		
	cat $all_tracks | _inner_search "$@"
}

shadd() {
	cat | shuf | add
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
		shift 1
        search "$@"
        ;;
    add)
        add
        ;;
	playlist)
		playlist "$2"
		;;
	clear)
		clr
		;;
	listall)
		listall
		;;
	shadd)
		shadd
		;;
	addf)
		addf
		;;
    *)
        printf %s\\n "not recognized"
        ;;
esac
