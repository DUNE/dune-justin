FROM centos/s2i-core-centos7:latest

RUN yum update -y
RUN yum install -y git
RUN yum install -y python36
RUN yum install -y python36-devel
RUN yum install -y mariadb-server
RUN yum install -y mariadb-devel
RUN yum install -y MySQL-python
RUN yum install -y gcc
RUN yum install -y make
RUN yum install -y bzip2-devel xz-devel libcurl-devel libjpeg-devel
RUN yum update -y

RUN python3 -m pip install mysqlclient
RUN python3 -m pip install wheel
RUN python3 -m pip install setuptools_rust
RUN python3 -m pip install rust
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install rucio

# RUN git clone https://github.com/DUNE/dune-wfs.git
# RUN ln -s dune-wfs/modules wfs
# RUN cd dune-wfs/agents; ln -s ../modules/modules wfs

COPY agents/wfs-info-collector /usr/sbin/justin-info-collector
COPY agents/wfs-finder         /usr/sbin/justin-finder
COPY agents/wfs-finder-fnal    /usr/sbin/justin-finder-fnal
COPY agents/wfs-job-factory    /usr/sbin/justin-job-factory
COPY agents/wfs-stage-cache    /usr/sbin/justin-stage-cache

RUN ls -l /usr/sbin/justin*

COPY agents/wfs-info-collector.service /usr/lib/systemd/system/justin-info-collector.service
COPY agents/wfs-finder.service         /usr/lib/systemd/system/justin-finder.service
COPY agents/wfs-finder-fnal.service    /usr/lib/systemd/system/justin-finder-fnal.service
COPY agents/wfs-job-factory.service    /usr/lib/systemd/system/justin-job-factory.service
COPY agents/wfs-stage-cache.service    /usr/lib/systemd/system/justin-stage-cache.service

COPY agents/wfs.logrotate /etc/logrotate.d/justin

COPY  genericjobs/run-jobsub-submit /var/lib/justin/
COPY  genericjobs/wfs-generic-job   /var/lib/justin/

RUN mkdir /usr/lib/python3.6/site-packages/justin
COPY modules/allocator.py /usr/lib/python3.6/site-packages/justin/
COPY modules/conf.py      /usr/lib/python3.6/site-packages/justin/
# COPY modules/justin_version.py /usr/lib/python3.6/site-packages/justin/
COPY modules/db.py        /usr/lib/python3.6/site-packages/justin/
COPY modules/events.py    /usr/lib/python3.6/site-packages/justin/
COPY modules/__init__.py  /usr/lib/python3.6/site-packages/justin/

RUN ls -l /usr/sbin/justin*
RUN ls -l /etc/logrotate.d/justin/

ENTRYPOINT ["/usr/sbin/justinEntrypoint.sh"]
