#!/usr/bin/env bash
set -e

# ls -l /etc/grid-security/	
# certbot --apache -d dune-wfs-test.cern.ch

which httpd
httpd -M
mod_wsgi-express module-config
pwd

whoami
echo "Starting apache ..."
httpd -D FOREGROUND

# certbot --apache -d wfs-pro.dune.hep.ac.uk -d wfs.dune.hep.ac.uk
