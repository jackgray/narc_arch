#!/bin/env bash

# sudo docker run -e ARANGO_RANDOM_ROOT_PASSWORD=1 -d --name arangodb-instance -p 8529:8529 arangodb

sudo docker run -p 8529:8529 -e ARANGO_ROOT_PASSWORD=r1t@_n311y -v arangodb:/data arangodb/enterprise:3.9.1 