#!/usr/bin/env bash
set -e

# ls -l /etc/grid-security/	
# certbot --apache -d dune-wfs-test.cern.ch

which httpd

pwd

whoami

httpd -D FOREGROUND

# certbot --apache -d wfs-pro.dune.hep.ac.uk -d wfs.dune.hep.ac.uk
