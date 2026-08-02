cat $RUCIO_HOME/etc/rucio.cfg

cat <<EOF >rucio-client-test.py
#!/usr/bin/env python3
import logging
import rucio.client.uploadclient
logging.basicConfig(level = logging.DEBUG)
client  = rucio.client.Client()
uc      = rucio.client.uploadclient.UploadClient(client)
print(uc)
EOF
chmod +x rucio-client-test.py
./rucio-client-test.py
ls -lt justin-jobs-production.proxy.pem
cat justin-jobs-production.proxy.pem

date --utc +'%b %d %H:%M:%S ====Finish justin-wrapper-job.sh===='
