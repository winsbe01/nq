
all_ids="$HOME/.config/nq/*.ids"
all_tracks="$HOME/.config/nq/*.tracks"
queuedir="$HOME/.config/nq"

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
	case "$1" in
		"")
			out=$queuedir"/queue"
			;;
		*)
			out=$queuedir"/$1"
			;;
	esac

    while read line; do
        grep -h "^`echo $line | cut -d ' ' -f 1`" $all_ids >> $out
    done
}

addf() {
    case "$1" in
        "")
            out=$queuedir"/queue"
            ;;
        *)
            out=$queuedir"/$1"
            ;;
    esac
	tmpfile=$(mktemp)
	cp $out $tmpfile
	clr "$1"
	cat | add "$1"
	cat $tmpfile | add "$1"
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

show() {
    case "$1" in
        "")
            out=$queuedir"/queue"
            ;;
        *)
            out=$queuedir"/$1"
            ;;
    esac

	while read line; do
		grep -h `echo $line | cut -d ';' -f 1` $all_tracks | print_track
	done < $out
}

edit() {
	tmpfile=$(mktemp)
	show "$1" > $tmpfile
	"${EDITOR:-nano}" $tmpfile
	clr "$1"
	cat "$tmpfile" | add "$1"
    case "$1" in
        "")
            echo "queue updated!"
            ;;
        *)
            echo "'$1' updated!"
            ;;
    esac
	rm "$tmpfile"
}

clr() {
    case "$1" in
        "")
            out=$queuedir"/queue"
            ;;
        *)
            out=$queuedir"/$1"
            ;;
    esac
	> $out
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
	cat | shuf | add "$1"
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
        add "$2"
        ;;
    edit)
        edit "$2"
        ;;
    show)
        show "$2"
        ;;
	clear)
		clr "$2"
		;;
	listall)
		listall
		;;
	shadd)
		shadd "$2"
		;;
	addf)
		addf "$2"
		;;
    *)
        printf %s\\n "not recognized"
        ;;
esac
