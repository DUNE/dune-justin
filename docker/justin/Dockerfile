# Build with something like this in the dune-justin top level directory:
#
# docker build -t justin:01 -f docker/justin/Dockerfile .
#
#FROM centos/s2i-core-centos7:latest
#FROM centos:centos7.9.2009
FROM centos:centos7

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

COPY agents/justin-info-collector /usr/sbin/
COPY agents/justin-finder         /usr/sbin/
COPY agents/justin-finder-fnal    /usr/sbin/
COPY agents/justin-job-factory    /usr/sbin/
COPY agents/justin-stage-cache    /usr/sbin/

COPY agents/justin-info-collector.service /usr/lib/systemd/system/
COPY agents/justin-finder.service         /usr/lib/systemd/system/
COPY agents/justin-finder-fnal.service    /usr/lib/systemd/system/
COPY agents/justin-job-factory.service    /usr/lib/systemd/system/
COPY agents/justin-stage-cache.service    /usr/lib/systemd/system/

COPY agents/justin.logrotate /etc/logrotate.d/justin.logrotate

COPY  genericjobs/run-jobsub-submit  /var/lib/justin/
COPY  genericjobs/justin-generic-job /var/lib/justin/

RUN mkdir /usr/lib/python3.6/site-packages/justin
COPY modules/allocator.py /usr/lib/python3.6/site-packages/justin/
COPY modules/conf.py      /usr/lib/python3.6/site-packages/justin/
COPY modules/justin_version.py /usr/lib/python3.6/site-packages/justin/
COPY modules/db.py        /usr/lib/python3.6/site-packages/justin/
#COPY modules/events.py    /usr/lib/python3.6/site-packages/justin/
COPY modules/__init__.py  /usr/lib/python3.6/site-packages/justin/

RUN mkdir -p /etc/justin.d
COPY docker/justin/database.conf /etc/justin.conf

COPY docker/justin/justinEntrypoint.sh /usr/sbin/
RUN mkdir -p /var/log/justin

RUN mkdir -p /docker-entrypoint-initdb.d
COPY database/justindb-create-tables.sql /docker-entrypoint-initdb.d/

ENTRYPOINT ["/usr/sbin/justinEntrypoint.sh"]
