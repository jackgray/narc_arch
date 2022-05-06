#!/bin/env bash

sudo docker run -e ARANGO_RANDOM_ROOT_PASSWORD=1 -d --name arangodb-instance -p 8529:8529 arangodb

