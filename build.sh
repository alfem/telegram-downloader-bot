#!/bin/sh
docker buildx create --name telegram-dl-bot --use
docker buildx build \
            --platform linux/amd64,linux/arm64,linux/arm/v7 \
            -t mitto98/telegram-downloader-bot:latest --push .