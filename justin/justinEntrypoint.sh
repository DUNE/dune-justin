#!/usr/bin/env bash
set -e

./justin/agents/justin-finder
./justin/agents/justin-stage-cache
./justin/agents/justin-info-collector
./justin/agents/justin-job-factory

tail -f /var/log/wfs/*
