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

justIN reads the per-RSE storage usage and quotas from Rucio for each named
quota, and uses that information when selecting the list of RSEs to attempt
to uploaded output files to. Each named quota has a page on the justIN
dashboard and they are all listed on the page Quotas which has a link from
the main page of the Dashboard. The per-RSE limits are shown on each 
named quota's page.

Each named quota is also associated with an HTCondor group and justIN reads
the config and effective quotas from HTCondor. These are visible on the 
named quota's page. On the page listing all the Rucio scopes that justIN
can manage are the HTCondor group associated with each scope. People with
justIN admin access can change these per-scope HTCondor groups to any 
group starting with the named quota's HTCondor group or the group itself.
For example, named quota dunepro has HTCondor group group_dune.prod and its 
scopes could be set to group_dune.prod.mcsim .

Each user and named quota has a processing enabled switch, set to enabled or
disabled. Admins can change this by going to the user's or named quota's
own page.

Each new workflow is now associated with a numeric campaign, with numbers
assigned in order by justIN. Each workflow can be assigned to a different
campaign by editing its settings on the page dedicated to that workflow. A
new list of all campaigns is available via the main page of the Dashboard.
The justin command and man page have been updated to include a
create-campaign subcommand which can be used to create a new campaign. When
creating workflows from the command line, the option --campaign-id can be
used to assign it to a particular existing campaign. If no campaign is 
specified, a new one is created specifically for that group. 
