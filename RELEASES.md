### 01.06 Release notes

This release has explicit reporting of output failures due to duplicate
files in the wrapper job log; the use of list_parent_dids() in
`justin-rucio-upload` to check for silent Rucio dataset failures and a new
event `JOB_ABORT_RUCIO_SILENT_FAILURE` which is generated when just failures
are detected; a new justin-shell container suitable for command line testing
within the container environment used by the justIN agents and services; a
`--production` option to `justin get-token` now allows the fetching of a
production team X.509 proxy instead of the read-only proxy available within
jobs.

However, the major change is the additional of the general Named Quotas 
mechanism. Each named quota matches the name of a Rucio account which justIN
can authenticate as. At the moment this is done by listing the justIN 
production DN as one of the X.509 identities of the account in Rucio. 

Each scope that justIN can use is associated with one named quota, and is
the Rucio account that owns that scope in Rucio. 

Each named quota is either associated with one user or with one WLCG Group.
For example the named quota amcnab_fnal_gov is owned by amcnab@fnal.gov and
dunele is associated with /dune/lowenergy and usable by people within that
WLCG group.

