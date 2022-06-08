## Services

The Workflow System provides services to respond to queries from users and
jobs. In most cases, queries update the [Workflow Database](database.md)
in some way.

Each service is currently implemented as an Apache CGI script written in
Python 3. The Apache configuration enables OpenSSL's support for X.509 Proxy
Certificates, and this allows 
clients to authenticate using X.509 certificates or grid style X.509
proxies of users or grid jobs. 

- wfa-cgi - [Workflow Allocator](workflow-allocator.md), which responds to queries from generic jobs
- wfdb-cgi - Workflow Database API, which responds to queries from the [workflow command](workflow-command.md)

The [Workflow Dashboard](dashboard.md) is implemented in the same way as the
other services, as a Python CGI script.
