#!/bin/bash
# Drop into each subdirectory and create a podcast feed.xml inside each
# Can then run http-server (npm install http-server; directory indexes are on by default)

files_base="/Volumes/Storage/downloads/get_iplayer"
script="`pwd`/podcast.py"

for dir in $files_base/*
do
    if [ -d "$dir" ]   # if dir is a directory
    then
       cd "$dir"
       title="`basename "$dir"`"
       $script "http://gerrard:8080/$title" "$title" "Description here"
    fi
done

http-server $files_base