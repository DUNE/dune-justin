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

ENTRYPOINT ["/usr/sbin/workflowEntrypoint.sh"]
