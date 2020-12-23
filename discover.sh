#!/bin/bash
# requesting data and writing the response to a file

export SPOTIPY_CLIENT_ID='4a42c140ceb94d6eba6a1cb1ad3e3753'
export SPOTIPY_CLIENT_SECRET='64a9762fbdcd43c8aecbacaf883b548a'
export SPOTIPY_REDIRECT_URI='https://localhost:8888'


python3 longer_discover_weekly.py $1 $2 $3
