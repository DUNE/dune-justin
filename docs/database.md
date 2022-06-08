## Workflow Database

The Workflow Database is the heart of the Workflow System. It holds cached
information about sites, storages, files, and replicas obtained from other
data sources; it receives requests to process data, and manages the state of
requests and their stages, the files they need to process, and the jobs
created to do the processing. 

By design the database's copy of all this information is transient, and
anything required for long term preservation must be exported. 

The database receives periodic updates from [agents](agents.md), 
[services](services.md), and can be examined using the
[dashboard](dashboard.md).

The database is implemented as a MySQL/Mariadb SQL database. A MySQL 
script to create a set of empty tables is in
wfdb-create-tables.sql in the databases subdirectory of the GitHub repo.
