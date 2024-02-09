# Dockerfile for AlmaLinux 9
#
FROM almalinux/almalinux:9

RUN yum update -y
RUN yum install -y git
#RUN yum install -y mariadb
RUN yum install -y python3-PyMySQL
RUN yum install -y gcc make which python3-pip
#RUN yum install -y bzip2-devel xz-devel libcurl-devel libjpeg-devel
#RUN yum update -y

#RUN python3 -m pip install mysqlclient
#RUN python3 -m pip install wheel
#RUN python3 -m pip install setuptools_rust
#RUN python3 -m pip install rust
#RUN python3 -m pip install --upgrade pip
RUN pip3 install rucio
RUN pip3 install metacat

COPY agents/justin-info-collector /usr/sbin/
COPY agents/justin-finder         /usr/sbin/
COPY agents/justin-finder-fnal    /usr/sbin/
COPY agents/justin-job-factory    /usr/sbin/

COPY agents/justin-info-collector.service /usr/lib/systemd/system/
COPY agents/justin-finder.service         /usr/lib/systemd/system/
COPY agents/justin-finder-fnal.service    /usr/lib/systemd/system/
COPY agents/justin-job-factory.service    /usr/lib/systemd/system/

RUN  mkdir            /opt/rucio/etc/
COPY agents/rucio.cfg /opt/rucio/etc/rucio.cfg

COPY agents/justin.logrotate /etc/logrotate.d/justin.logrotate

RUN mkdir -p /var/lib/justin
COPY agents/justin-wrapper-job /var/lib/justin/

RUN mkdir /usr/lib/python3.9/site-packages/justin
COPY modules/__init__.py       /usr/lib/python3.9/site-packages/justin/
COPY modules/justin_version.py /usr/lib/python3.9/site-packages/justin/

#RUN mkdir -p /etc/justin.d
#COPY docker/justin/database.conf /etc/justin.conf
#
#RUN mkdir -p /docker-entrypoint-initdb.d
#COPY database/justindb-create-tables.sql /docker-entrypoint-initdb.d/

COPY docker/justin/justinEntrypoint.sh /usr/sbin/

# MOUNT LOGS FROM HOST???
#RUN mkdir -p /var/log/justin
RUN mkdir -p /var/run/justin/last-updates

ENTRYPOINT ["/usr/sbin/justinEntrypoint.sh"]
