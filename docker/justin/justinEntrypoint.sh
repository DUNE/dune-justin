#!/usr/bin/env bash
set -e

/usr/sbin/justin-finder
/usr/sbin/justin-stage-cache
/usr/sbin/justin-info-collector
/usr/sbin/justin-job-factory

ls -l /var/log/

tail -f /var/log/wfs/*