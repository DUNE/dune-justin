#!/usr/bin/env bash
set -e

/usr/sbin/justin-finder
#/usr/sbin/justin-finder-fnal
/usr/sbin/justin-info-collector
#/usr/sbin/justin-job-factory

ls -l /var/log/

tail -f /var/log/justin/*
