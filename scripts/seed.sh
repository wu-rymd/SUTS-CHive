#!/bin/bash
school_id=$(curl -H 'Content-Type: application/json' -d '{"name":"Cool High School", "address":"500 Fonz Pl", "email": "the.fonz@cool.edu","phone":"323-888-8888"}' -X POST localhost:5000/schools | jq -r '.id')
user_id=$(curl -H 'Content-Type: application/json' -d '{"first_name":"Jay", "last_name":"Zee","username": "jay-z","password":"immaballah","school":"Cool High School","email":"jayz@ballers.gov"}' -X POST localhost:5000/user | jq '.id')
club_id=$(curl -H 'Content-Type: application/json' -d '{"name":"CHEESE", "school_id":"${school_id}","description": "hey its a club about cheese okay","img_type":"IMAGE"}' -X POST localhost:5000/club | jq '.id')

curl -X POST localhost:5000/subscribe?user_id=${user_id}&club_id=${club_id}
