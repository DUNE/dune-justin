#!/bin/bash
#
# This seems to work when run inside a singularity container:
# 
# singularity shell -B /cvmfs \
# /cvmfs/singularity.opensciencegrid.org/fermilab/fnal-wn-sl7:osg3.6 /bin/bash
#

whoami
uname -a
cat /etc/redhat-release
printenv
which pip3
python3 --version
echo
echo
echo
## Inside the above singularity container, you can use the rucio stuff 
## installed by this script in  your own process environment by just doing 
## these three exports
export RUCIO_HOME=$PWD/rucio-local
export PATH="$RUCIO_HOME/bin:$PATH"
export PYTHONPATH="$RUCIO_HOME/lib/python3.6/site-packages:/usr/lib64/python3.6/site-packages"
##
##


mkdir -p $RUCIO_HOME/bin $RUCIO_HOME/etc

pip3 install --no-cache-dir --prefix $RUCIO_HOME \
             --ignore-installed rucio-clients==1.26.9

echo "Write config to $RUCIO_HOME/etc/rucio.cfg"
cat <<EOF > $RUCIO_HOME/etc/rucio.cfg
[client]
rucio_host = https://dune-rucio.fnal.gov
auth_host = https://auth-dune-rucio.fnal.gov
ca_cert = /etc/grid-security/certificates
account = amcnab
auth_type = x509_proxy
request_retries = 3
EOF

which rucio
$RUCIO_HOME/bin/rucio -v --version
$RUCIO_HOME/bin/rucio -v --timeout 60 whoami

onemegabyte=`date +"1mb%s"`

dd if=/dev/zero of=onemegabyte bs=1024 count=1000

$RUCIO_HOME/bin/rucio -v -a test upload --rse FNAL_DCACHE_TEST --lifetime 1 \
 --scope test --register-after-upload \
 --name $onemegabyte onemegabyte

$RUCIO_HOME/bin/rucio -v list-file-replicas test:$onemegabyte
