#!/bin/bash

cd qaas
docker compose up -d --build

cd ..

cd shellrage
docker compose up -d --build
cd ..

