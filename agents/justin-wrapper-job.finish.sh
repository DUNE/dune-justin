cat $RUCIO_HOME/etc/rucio.cfg

cat <<EOF >rucio-client-test.py
#!/usr/bin/env python3
import logging
import rucio.client.uploadclient
logging.basicConfig(level = logging.DEBUG)
client  = rucio.client.Client()
uc      = rucio.client.uploadclient.UploadClient(client)
EOF
chmod +x rucio-client-test.py
./rucio-client-test.py

date --utc +'%b %d %H:%M:%S ====Finish justin-wrapper-job.sh===='
