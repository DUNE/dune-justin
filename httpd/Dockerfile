FROM centos:7

USER root

RUN yum update -y
RUN yum -y install httpd httpd-tools mod_ssl openssl expect
RUN yum install -y epel-release
RUN yum install -y certbot python2-certbot-apache

RUN ls -l /etc/httpd/

COPY dashboard/wfs-wsgi-dashboard /var/www/wsgi/justin-wsgi-dashboard-dev
COPY services/wfs-wsgi-import-script /var/www/wsgi/justin-wsgi-import-script
COPY services/wfs-wsgi-commands /var/www/wsgi/justin-wsgi-commands
COPY services/wfs-wsgi-allocator /var/www/wsgi/justin-wsgi-allocator
COPY services/wfs.conf /etc/httpd/conf.d/

USER 1001

ENTRYPOINT ["/usr/local/apache2/httpdEntrypoint.sh"]
