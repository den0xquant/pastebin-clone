#!/bin/bash

docker-compose --env-file .dev.env --file docker/docker-compose.yml --file docker/docker-compose.dev.yml up -d app
