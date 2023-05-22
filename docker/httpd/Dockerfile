FROM centos:7

USER root
EXPOSE 80/tcp

RUN yum update -y
RUN yum install -y python3 python3-devel python-devel gcc
RUN yum install -y wget httpd httpd-devel httpd-tools mod_ssl openssl expect python3-mod_wsgi

RUN yum install -y epel-release lcg-CA wlcg-repo
RUN yum install -y http://repository.egi.eu/sw/production/umd/4/centos7/x86_64/updates/umd-release-4.1.3-1.el7.centos.noarch.rpm
RUN yum install -y http://linuxsoft.cern.ch/wlcg/centos7/x86_64/wlcg-repo-1.0.0-1.el7.noarch.rpm
RUN yum install -y wlcg-vobox
RUN yum install -y mod_wsgi

# RUN yum install -y certbot python2-certbot-apache
RUN yum update -y

COPY dashboard/justin-wsgi-dashboard    /var/www/wsgi/
COPY services/justin-wsgi-import-script /var/www/wsgi/
COPY services/justin-wsgi-ui            /var/www/wsgi/
#COPY services/justin-wsgi-commands      /var/www/wsgi/
COPY services/justin-wsgi-allocator     /var/www/wsgi/

COPY services/justin.conf /etc/httpd/conf.d/

COPY docs/*.md /var/www/html/docs/

RUN mkdir -p /etc/httpd/bin
COPY docker/httpd/httpdEntrypoint.sh /etc/httpd/bin/

#COPY docker/httpd/conf.modules.d/* /etc/httpd/conf.modules.d/

#COPY docker/certificates/wfs.dune.hep.ac.uk/ /etc/grid-security/certificates/wfs.dune.hep.ac.uk
#COPY docker/certificates/ /etc/grid-security/
## ADD docker/certificates/wfs.dune.hep.ac.uk.tar.gz /etc/grid-security/certificates/

# USER 1001

ENTRYPOINT ["/etc/httpd/bin/httpdEntrypoint.sh"]
