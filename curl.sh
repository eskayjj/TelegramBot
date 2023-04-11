#!/bin/sh

curl -X 'POST' \
  'http://35.239.210.99:8080/predict/640704fee9e9c81d970e5096' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@<FILENAME>;type=image/jpeg'