
all_ids="$HOME/.config/nq/*.ids"
all_tracks="$HOME/.config/nq/*.tracks"
queue="$HOME/.config/nq/queue"

play() {
    echo "play" | nc localhost 55555
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
    grep -i "$1" $all_tracks | awk -F';;' '{ print substr($1,1,8) "  " $4 "/" $3 "/" $5 " - " $6 }' | sort -k 2
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
        search $2
        ;;
    add)
        add
        ;;
    *)
        printf %s\\n "not recognized"
        ;;
esac
