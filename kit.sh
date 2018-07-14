#!/usr/bin/env bash

if [ "$1" = "up" ]
then
    echo "Starting docker development server..."
    docker-compose -f docker-compose-dev.yml up
elif [ "$1" = "down" ]
then
    echo "Stoping docker development server..."
    docker-compose -f docker-compose-dev.yml down
elif [ "$1" = "ps" ]
then
    docker-compose -f docker-compose-dev.yml ps
elif [ "$1" = "build" ]
then
    echo "Building docker image..."
    docker-compose -f docker-compose-dev.yml build
elif [ "$1" = "rebuild" ]
then
    echo "Rebuilding docker development server..."
    docker-compose -f docker-compose-dev.yml up --build
elif [ "$1" = "test:api" ]
then
    echo "Running test..."
elif [ "$1" = "db:create" ]
then
    echo "Creating database"
    docker-compose -f docker-compose-dev.yml run users python manage.py recreate_db
elif [ "$1" = "db:seed" ]
then
    echo "Seeding database"
else
    echo "Nothing to do..."
fi
