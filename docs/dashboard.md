# justIN dashboard

The justIN dashboard gives convenient views of the contents of the 
[justIN database](database.md).

It is currently implemented as an Apache WSGI application written in
Python 3 and accessible at 
[https://justin.dune.hep.ac.uk/dashboard/](https://justin.dune.hep.ac.uk/dashboard/).

The dashboard uses the [justIN database](database.md) section
of the configuration files, and also the [cilogon] section which has client 
details for OIDC calls to CILogon:

- client_id - ID string of a registered client
- secret - secret for the registered client

