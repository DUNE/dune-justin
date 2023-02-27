# Services

justIN provides services to respond to queries from users and
jobs. In most cases, queries update the [justIN database](database.md)
in some way.

Each service is implemented as a WSGI/mod_wsgi script written in Python 3. 

- justin-wsgi-allocator - [allocator service](services.allocator.md), which responds to queries from generic jobs
- justin-wsgi-commands - justIN commands service, which responds to queries from the [justin command](justin_command.md)

The [justIN dashboard](dashboard.md) is also implemented as a WSGI service.
