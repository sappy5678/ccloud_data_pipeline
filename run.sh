#!/bin/sh
ssh -4 -L 10200:localhost:10200 sappy@whisky.nlplab.cc -p 2222 -N -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o IdentityFile=/.ssh/docker_id_rsa &

python ./nltk_install.py

uvicorn fastapi_test:app --host="0.0.0.0" --port="8080"


