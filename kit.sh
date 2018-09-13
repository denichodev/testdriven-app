#!/usr/bin/env bash

if [ "$1" = "up" ]
then
    echo "Starting docker development server..."
    docker-compose -f docker-compose-dev.yml up
elif [ "$1" = "deploy" ]
then
    echo "Switching env to production..."
    eval $(docker-machine env testdriven-prod)
    echo "Building & deploying..."
    docker-compose -f docker-compose-prod.yml up -d --build
    echo "Success... switching to unset env"
    eval $(docker-machine env -u)
else
    echo "Nothing to do..."
fi
