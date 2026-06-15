#!/bin/bash

BASE="/opt/lentra/infra"

mkdir -p $BASE/lentra/api/routes
mkdir -p $BASE/lentra/api/schemas
mkdir -p $BASE/lentra/api/deps

mkdir -p $BASE/lentra/bot
mkdir -p $BASE/lentra/bot/handlers
mkdir -p $BASE/lentra/bot/services

mkdir -p $BASE/lentra/db/models
mkdir -p $BASE/lentra/db/repositories
mkdir -p $BASE/lentra/db/services
mkdir -p $BASE/lentra/db/migrations

mkdir -p $BASE/lentra/core/ranking
mkdir -p $BASE/lentra/core/search
mkdir -p $BASE/lentra/core/filters

mkdir -p $BASE/lentra/common

echo "STRUCTURE CREATED"
