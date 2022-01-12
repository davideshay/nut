#!/bin/sh
token=AYSJuJzA1xGDaZy
APIKEY=il1api1121e2ddcf370fa845a981cc1fe3736b6b4b8a281fa058
title="NUT UPS monitor"
message=$1
priority=10
URL="http://gotify.gotify/message?token=$token"
curl -s -S --data '{"message": "'"${message}"'", "title": "'"${title}"'", "priority":'"${priority}"', "extras": {"client::display": {"contentType": "text/markdown"}}}' -X POST -H Content-Type:application/json "$URL"
JSONDATA=$( jq -n -j \
  --arg api "$APIKEY" \
  --arg et "ALERT" \
  --arg ak "$title" \
  --arg sm "$title" \
  --arg dt "$message" \
  '{apiKey: $api, eventType: $et, alertKey: $ak, summary: $sm, details: $dt}' )
JOUT="$(mktemp)"
echo $JSONDATA >$JOUT
curl -s -S -H "Content-Type: application/json" --data @$JOUT https://api.ilert.com/api/events
