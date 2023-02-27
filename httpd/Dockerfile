FROM centos/httpd-24-centos7

USER root

RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y certbot python2-certbot-apache mod_ssl

USER 1001

ENTRYPOINT ["/usr/local/apache2/httpdEntrypoint.sh"]
