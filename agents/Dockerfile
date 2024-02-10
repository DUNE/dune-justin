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
# agents/build-agents-container
#
# Run agents with provided systemd .service files
#

FROM almalinux:9
RUN useradd --uid 1026 --user-group dunejustin
RUN yum update -y

RUN yum install -y git
RUN yum install -y python3-PyMySQL python3-pyyaml
RUN yum install -y gcc make which nano procps-ng python3-pip

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
 
RUN  mkdir -p         /opt/rucio/etc/
COPY agents/rucio.cfg /opt/rucio/etc/rucio.cfg

RUN mkdir -p /var/lib/justin
COPY agents/justin-wrapper-job /var/lib/justin/

RUN mkdir /usr/lib/python3.9/site-packages/justin
COPY modules/__init__.py       /usr/lib/python3.9/site-packages/justin/
COPY modules/justin_version.py /usr/lib/python3.9/site-packages/justin/

RUN mkdir -p /var/run/justin/last-updates
