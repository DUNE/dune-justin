#!/usr/bin/env bash
set -e

httpd -D FOREGROUND

# certbot --apache -d wfs-pro.dune.hep.ac.uk -d wfs.dune.hep.ac.uk
