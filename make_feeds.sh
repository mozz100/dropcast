#!/bin/bash
# These three variables are important
files_base="/Volumes/Storage/downloads/get_iplayer"
script="$HOME/Documents/Source/personal/dropcast/podcast.py"
base_url="http://gerrard:8080"

for dir in $files_base/*
# Drop into each subdirectory and create a podcast feed.xml inside each
# Can then run http-server (npm install http-server; directory indexes are on by default)
do
    if [ -d "$dir" ]   # if dir is a directory
    then
       cd "$dir"
       title="`basename "$dir"`"
       $script "$base_url/$title" "$title" "Description here"
    fi
done