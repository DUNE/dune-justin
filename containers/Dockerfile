# Dockerfile for justIN agents on AlmaLinux 9
#
# Copyright 2013-24 
# Raja Nandakumar for UKRI Science and Technology Facilities Council
# Andrew McNab for the University of Manchester
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Build with:
#
# cd dune-justin
# docker/build-justin-container
#
# Run agents with provided systemd .service files
#

FROM almalinux:9

# Setup dunejustin, yum files, and update the base OS
RUN useradd --uid 1026 --user-group dunejustin
RUN dnf install -y epel-release
RUN dnf config-manager --set-enabled crb
RUN yum -y install \
 https://research.cs.wisc.edu/htcondor/repo/10.x/htcondor-release-current.el9.noarch.rpm
RUN yum update -y

# Install the RPMs we need
RUN yum install -y git joe util-linux-user
RUN yum install -y mariadb python3-PyMySQL python3-pyyaml
RUN yum install -y make which nano procps-ng python3-pip
RUN yum install -y python3-devel gcc swig openssl-devel

RUN yum install -y httpd mod_ssl 
# Force prefork rather than a threaded mpm module
RUN sed -i -e 's:^LoadModule mpm.*:#&:' -e \
 's:^#LoadModule mpm_prefork_module.*:LoadModule mpm_prefork_module modules/mod_mpm_prefork.so:' \
 /etc/httpd/conf.modules.d/00-mpm.conf 
# The container image mod_ssl does not have a %post to generate these files:
RUN ln -sf /etc/grid-security/justin.cert.pem /etc/pki/tls/certs/localhost.crt
RUN ln -sf /etc/grid-security/justin.key.pem /etc/pki/tls/private/localhost.key
RUN yum install -y python3-mod_wsgi



RUN yum install -y python3-markdown
RUN yum install -y munge

# With 10.x this pulls in condor itself and the voms clients
RUN yum install -y python3-condor

# Some things do not have suitable RPMs
RUN pip3 install rucio
RUN pip3 install metacat
RUN pip3 install pygal==3.0.0

# We want recent version with Chris Haen's X.509 proxy updates
# Needs python3-devel gcc swig openssl-devel RPMs
RUN pip3 install M2Crypto==0.39.0

# Copy justIN scripts and configs into place
COPY agents/justin-info-collector /usr/sbin/
COPY agents/justin-finder         /usr/sbin/
COPY agents/justin-finder-fnal    /usr/sbin/
COPY agents/justin-job-factory    /usr/sbin/

COPY agents/justin-info-collector.service /usr/lib/systemd/system/
COPY agents/justin-finder.service         /usr/lib/systemd/system/
COPY agents/justin-finder-fnal.service    /usr/lib/systemd/system/
COPY agents/justin-job-factory.service    /usr/lib/systemd/system/
 
RUN  mkdir -p         /opt/rucio/etc/
COPY agents/rucio.cfg /opt/rucio/etc/rucio.cfg

RUN mkdir -p /var/lib/justin
COPY agents/justin-wrapper-job /var/lib/justin/

RUN mkdir /usr/lib/python3.9/site-packages/justin
COPY modules/__init__.py       /usr/lib/python3.9/site-packages/justin/
COPY modules/justin_version.py /usr/lib/python3.9/site-packages/justin/

RUN mkdir -p /var/www/wsgi/ /var/www/html/docs/
RUN mkdir -p /var/run/justin/last-updates/
 
COPY services/justin-wsgi-import-script /var/www/wsgi/
COPY services/justin-wsgi-ui            /var/www/wsgi/
COPY services/justin-wsgi-allocator     /var/www/wsgi/
COPY services/httpd.justin.conf         /etc/httpd/conf.d/
COPY dashboard/justin-get-output        /var/lib/justin/
COPY dashboard/justin-wsgi-dashboard    /var/www/wsgi/
COPY dashboard/*.png                    /var/www/html/
COPY docs/*.md                          /var/www/html/docs/

COPY agents/02_dune_condor.conf         /etc/condor/config.d/

COPY containers/start-justin-httpd          /usr/sbin/
COPY containers/start-justin-finder         /usr/sbin/
COPY containers/start-justin-job-factory    /usr/sbin/
COPY containers/start-justin-info-collector /usr/sbin/
