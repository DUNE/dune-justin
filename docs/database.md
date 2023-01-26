## justIn database

The justIn database is the heart of the justIn workflow system. It holds cached
information about sites, storages, files, and replicas obtained from other
data sources; it receives requests to process data, and manages the state of
requests and their stages, the files they need to process, and the jobs
created to do the processing. 

By design the database's copy of all this information is transient, and
anything required for long term preservation must be exported. 

The database receives periodic updates from [agents](agents.md), 
[services](services.md), and can be examined using the
[dashboard](dashboard.md).

The database is implemented as a MySQL/Mariadb SQL database. 

### Tables

- allocations - one row each time a file is allocated to a job
- bootstraps - scripts from users to be executed by generic jobs
- events - a log of fine grained events within the system
- files - input files associcated with each stage of each request
- jobs - jobs created by the Generic Job Factory
- jobs_logs - logs from the bootstrap scripts that generic jobs run 
- replicas - replica RSEs and PFNs obtained from Rucio
- replicas_pins - used by the FNAL Finder Agent to manage pins
- requests - workflows submitted to the system for processing
- sites - site info obtained from the OSG Pilot Factory configuration
- sites_storages - distances between sites and storages
- stages - stages within each request
- stages_output_storages - preferred output RSEs for each stage
- stages_outputs - wildcards to find output files of bootstrap scripts
- storages - RSE info obtained from Rucio
- users - user info obtained from Rucio
- x509 - X.509 DNs associated with each user

A MySQL script to create a set of empty tables is in
justindb-create-tables.sql in the databases subdirectory of the GitHub repo,
and shows the full definition of each table.

### Configuration

The global justIn configuration can include a [database] section which may
include some or all of the following options. Default values are shown in
brackets.

- hostname - the host name of the MySQL/MariaDB service (localhost)
- username - the username to use (root)
- password - the password to use (none)
- db - the name of the database (justindb)
