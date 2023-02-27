FROM centos:7

USER root

RUN yum update -y
RUN yum -y install httpd httpd-tools mod_ssl openssl expect
RUN yum install -y epel-release
RUN yum install -y certbot python2-certbot-apache

COPY dashboard/justin-wsgi-dashboard    /var/www/wsgi/
COPY services/justin-wsgi-import-script /var/www/wsgi/
COPY services/justin-wsgi-commands      /var/www/wsgi/
COPY services/justin-wsgi-allocator     /var/www/wsgi/

COPY services/justin.conf /etc/httpd/conf.d/

COPY docs/*.md /var/www/html/docs/

COPY docker/httpd/httpdEntrypoint.sh /usr/local/apache2/
RUN ls -l /usr/local/apache2/

USER 1001

ENTRYPOINT ["/usr/local/apache2/httpdEntrypoint.sh"]
