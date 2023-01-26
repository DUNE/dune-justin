## Services

justIn provides services to respond to queries from users and
jobs. In most cases, queries update the [justIn database](database.md)
in some way.

Each service is implemented as a WSGI/mod_wsgi script written in
Python 3. The Apache configuration enables OpenSSL's support for X.509 Proxy
Certificates, and this allows 
clients to authenticate using X.509 certificates or grid style X.509
proxies of users or grid jobs. 

- justin-wsgi-allocator - [Allocator Service](workflow-allocator.md), which responds to queries from generic jobs
- justin-wsgi-commands - justIn commands service, which responds to queries from the [justin command](workflow-command.md)

The [justIn dashboard](dashboard.md) is currently implemented as a Python3 
CGI script.
