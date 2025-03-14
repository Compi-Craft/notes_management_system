#!/bin/bash

IMAGE_NAME="notes-management-project"
CONTAINER_NAME="notes-management-container"
PORT="8000"

echo "Building Docker image..."
docker build -t $IMAGE_NAME .

if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping existing container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

echo "Running Docker container..."
docker run -d -p $PORT:8000 --name $CONTAINER_NAME $IMAGE_NAME

echo "Active containers:"
docker ps
