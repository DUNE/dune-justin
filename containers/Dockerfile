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
## Nasty hack to get 10.0 not really 10.x!
#RUN sed -i 's/10.x/10.0/' /etc/yum.repos.d/htcondor*.repo
#RUN curl https://research.cs.wisc.edu/htcondor/repo/keys/HTCondor-10.0-Key \
#  > /etc/pki/rpm-gpg/RPM-GPG-KEY-HTCondor-10.0
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
RUN ln -sf /etc/justin-secrets/justin.cert.pem /etc/pki/tls/certs/localhost.crt
RUN ln -sf /etc/justin-secrets/justin.key.pem /etc/pki/tls/private/localhost.key
RUN yum install -y python3-mod_wsgi

RUN yum install -y python3-markdown
RUN yum install -y munge

# Install an updatable snapshot of the current CA files
COPY containers/trustanchors.repo /etc/yum.repos.d/
RUN yum install -y ca_policy_igtf-classic

# We only install crond for the automatic update of VOMS proxies
# Unless we have another use for it, it can go away when they do
# /usr/sbin/crond has to be started by each /usr/sbin/start-justin-* script
RUN yum install -y cronie voms-clients
COPY agents/justin-create-x509-proxies /etc/cron.daily/
RUN mkdir -p /etc/grid-security/vomsdir/dune /etc/vomses
RUN /bin/echo -e '/DC=org/DC=incommon/C=US/ST=Illinois/O=Fermi Research Alliance/CN=voms1.fnal.gov\n/C=US/O=Internet2/CN=InCommon RSA IGTF Server CA 3' >/etc/grid-security/vomsdir/dune/voms1.fnal.gov.lsc
RUN /bin/echo -e '/DC=org/DC=incommon/C=US/ST=Illinois/O=Fermi Research Alliance/CN=voms2.fnal.gov\n/C=US/O=Internet2/CN=InCommon RSA IGTF Server CA 3' >/etc/grid-security/vomsdir/dune/voms2.fnal.gov.lsc
RUN /bin/echo -e '"dune" "voms1.fnal.gov" "15042" "/DC=org/DC=incommon/C=US/ST=Illinois/O=Fermi Research Alliance/CN=voms1.fnal.gov" "dune"' >/etc/vomses/dune-voms1.fnal.gov
RUN /bin/echo -e '"dune" "voms2.fnal.gov" "15042" "/DC=org/DC=incommon/C=US/ST=Illinois/O=Fermi Research Alliance/CN=voms1.fnal.gov" "dune"' >/etc/vomses/dune-voms2.fnal.gov

# With HTCondor 10.x this pulls in condor itself and the voms clients
RUN yum install -y python3-condor

# Some things do not have suitable RPMs
RUN pip3 install rucio
RUN pip3 install metacat
RUN pip3 install pygal==3.0.0

# We want recent version with Chris Haen's X.509 proxy updates
# Needs python3-devel gcc swig openssl-devel RPMs
RUN pip3 install M2Crypto==0.39.0

# Copy justIN scripts and configs into place
COPY database/justin-check-db     /usr/sbin/
COPY agents/justin-info-collector /usr/sbin/
COPY agents/justin-finder         /usr/sbin/
COPY agents/justin-finder-fnal    /usr/sbin/
COPY agents/justin-job-factory    /usr/sbin/

COPY agents/justin-info-collector.service /usr/lib/systemd/system/
COPY agents/justin-finder.service         /usr/lib/systemd/system/
COPY agents/justin-finder-fnal.service    /usr/lib/systemd/system/
COPY agents/justin-job-factory.service    /usr/lib/systemd/system/

RUN  mkdir -p             /opt/rucio/etc/
COPY containers/rucio.cfg /opt/rucio/etc/rucio.cfg

RUN mkdir -p /var/lib/justin
COPY agents/justin-wrapper-job /var/lib/justin/

RUN mkdir /usr/lib/python3.9/site-packages/justin
COPY modules/__init__.py       /usr/lib/python3.9/site-packages/justin/
COPY modules/justin_version.py /usr/lib/python3.9/site-packages/justin/
COPY modules/events_list.py    /usr/lib/python3.9/site-packages/justin/

RUN mkdir -p /var/www/wsgi/ /var/www/html/docs/
RUN mkdir -p /var/run/justin/last-updates/ /etc/justin.d/

COPY containers/users.conf              /etc/justin.d/ 
COPY services/justin-wsgi-import-script /var/www/wsgi/
COPY services/justin-wsgi-ui            /var/www/wsgi/
COPY services/justin-wsgi-allocator     /var/www/wsgi/
COPY services/httpd.justin.conf         /etc/httpd/conf.d/
COPY dashboard/justin-get-output        /var/lib/justin/
COPY dashboard/justin-wsgi-dashboard    /var/www/wsgi/
COPY dashboard/*.png                    /var/www/html/
COPY *.md                               /var/www/html/docs/
COPY docs/*.md                          /var/www/html/docs/

COPY containers/02_dune_condor.conf     /etc/condor/config.d/
COPY containers/justin-client.cnf       /etc/my.cnf.d/

COPY containers/start-justin-httpd          /usr/sbin/
COPY containers/start-justin-finder         /usr/sbin/
COPY containers/start-justin-job-factory    /usr/sbin/
COPY containers/start-justin-info-collector /usr/sbin/

