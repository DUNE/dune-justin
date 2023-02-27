FROM centos:7

USER root

RUN yum update -y
RUN yum -y install httpd httpd-tools mod_ssl openssl expect
RUN yum install -y epel-release
RUN yum install -y certbot python2-certbot-apache

COPY dashboard/justin-wsgi-dashboard /var/www/wsgi/justin-wsgi-dashboard-dev

USER 1001

ENTRYPOINT ["/usr/local/apache2/httpdEntrypoint.sh"]
