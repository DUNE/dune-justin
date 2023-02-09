#!/usr/bin/env bash
set -e

./justin/agents/wfs-finder
./justin/agents/wfs-stage-cache
./justin/agents/wfs-info-collector
./justin/agents/wfs-job-factory

tail -f /var/log/wfs/*
