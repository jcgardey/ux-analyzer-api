#!/bin/sh

docker build -t jcgardey/ux-analyzer-api ./ux-analyzer-api --no-cache
docker push jcgardey/ux-analyzer-api

docker build -t jcgardey/ux-analyzer ./ux-analyzer --no-cache
docker push jcgardey/ux-analyzer