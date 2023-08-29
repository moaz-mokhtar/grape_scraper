#!/usr/bin/env bash

# set -xeu

# http://127.0.0.1:8000
PORT=8000
# HOST=localhost
HOST=127.0.0.1
URL=http://$HOST:$PORT
echo $URL

echo "\n\n==========================="
echo "Healthcheck, endpoint 'GET /'"
curl $URL



echo "\n\n==========================="
echo "Scrape data and save to db, endpoint 'GET /scrape/'"
curl $URL/scrape/


# echo "\n\n==========================="
# echo "Get all scraped data from db, endpoint 'GET /all/'"
# curl $URL/all/



