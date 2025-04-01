#!/usr/bin/env bash
docker build -t ds-backend . && docker run -v .:/app -p 8080:8080 ds-backend
