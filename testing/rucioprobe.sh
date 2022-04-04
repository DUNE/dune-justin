#!/bin/bash

whoami
uname -a
cat /etc/redhat-release
printenv

export RUCIO_LOCAL=$PWD/rucio-local
export PATH="$PATH:$RUCIO_LOCAL/bin"
export PYTHONPATH="$RUCIO_LOCAL/lib/python3.8/site-packages"
export X509_USER_PROXY=${X509_USER_PROXY:-/tmp/x509up_u`id -u`}

mkdir -p $RUCIO_LOCAL/bin
# Have to create symbolic link since cvmfs path 
# is too long for hash-bang at the start of a script
ln -sf /cvmfs/fermilab.opensciencegrid.org/packages/external/python/3.8.8/linux-scientific7-x86_64-gcc-8.2.0-x7eyi5xeluhxm3nzllayh4lsmdz3pfai/bin/python3.8 \
  $RUCIO_LOCAL/bin/python38

curl --insecure https://bootstrap.pypa.io/get-pip.py > get-pip.py
$RUCIO_LOCAL/bin/python38 get-pip.py --prefix $PWD/rucio-local --ignore-installed

# DOES NOT WORK WITH RUCIO 1.27 !!!
pip3.8 install --prefix $RUCIO_LOCAL --ignore-installed rucio-clients==1.26

cat <<EOF > $RUCIO_LOCAL/etc/rucio.cfg
[client]
rucio_host = https://dune-rucio.fnal.gov
auth_host = https://auth-dune-rucio.fnal.gov
ca_cert = /etc/grid-security/certificates
account = amcnab
auth_type = x509_proxy
client_x509_proxy = \$X509_USER_PROXY
request_retries = 3
EOF

head $RUCIO_LOCAL/bin/rucio
ls -l /cvmfs/fermilab.opensciencegrid.org/packages/external/python/3.8.8/linux-scientific7-x86_64-gcc-8.2.0-x7eyi5xeluhxm3nzllayh4lsmdz3pfai/bin/

rucio --version
rucio --timeout 60 --config $RUCIO_LOCAL/etc/rucio.cfg whoami
