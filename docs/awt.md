# Automated Workflow Tests

justIN's Automated Workflow Tests (AWT) test the reading and writing to 
storages from jobs, in the environment seen by user jobscripts. 

The 
[AWT results page](https://justin.dune.hep.ac.uk/dashboard/?method=awt-results)
shows site vs storage results for the download and upload tests run in jobs
at each site. The text on the page explains how red, green and orange
colours show whether the tests were successful for each combination of site
and storage. The "Last AWT job" column shows how long ago an AWT job ran
at each site and reported results, and so tests whether the sites are
accessilble to justIN jobs. It also has a link to that job's page on the 
justIN dashboard.

Generic jobs are tagged for AWT and targetted at each known 
[DUNE site](https://justin.dune.hep.ac.uk/dashboard/?method=list-sites),
whether it is enabled for user jobs or not.

The 
[AWT Request](https://justin.dune.hep.ac.uk/dashboard/?method=show-request&request_id=1)
is used to manage the jobs. It uses the metadata query
`rucio-dataset testpro:awt` to find files in the testpro:awt Rucio dataset. 
The [justIN finder agent](/docs/agents.finder.md) looks for new files in
that dataset every two hours and caches the new file's replicas at that point.
This means that if a new file is to added for the tests, it should already be
replicated to the desired RSEs before it is added the testpro:awt dataset.
When adding a new RSE, a rule for that RSE also needs to be added to the 
testpro:awt dataset. 

When an AWT-tagged generic job starts at a site, it contacts the 
[justIN allocator](/docs/services.allocator.md) and requests a jobscript
to execute in the normal way. The allocator recognises that the job is
tagged for AWT and returns an additional file with a list of RSEs to be
tested. This file is accessible to the AWT
jobscript at `$JUSTIN_PATH/justin-awt-rse-list.txt` and its contents are
logged to the jobscript's log file. Each line of that file contains the name
of an RSE to test, the upload protocol to use, and the root PFN of a replica
of a file in the testpro:awt dataset on that RSE which can be used for the
read test. Where there are mutiple files with suitable replicas on an RSE,
the one most recently cached from Rucio by the justIN finder agent is used. 
The upload protocol choice takes into account whether the site is considered
to be on the RSE's LAN or WAN, based on distance=0 for LAN. If a storage has
no replicas of files in testpro:awt then it is ignored.

The jobscript is taken from the single stage of the AWT request and is 
visible at the foot of 
[that stage's page](https://justin.dune.hep.ac.uk/dashboard/?method=show-stage&request_id=1&stage_id=1).

The production VOMS proxy normally used by the generic job for file uploads
is made available to the AWT jobscript at `$JUSTIN_PATH/awt-proxy.pem` and
this is currently used for both read and write tests. `voms-proxy-info -all`
is run by the jobscript so the proxy's details can be checked.

The jobscript loops through `$JUSTIN_PATH/justin-awt-rse-list.txt` doing

    xrdcp --force --nopbar --verbose "$read_pfn" "downloaded.txt"

and 

    rucio --verbose upload --rse $rse_name --protocol $write_protocol \
          --scope testpro --lifetime 86400 --name $fn $fn

where `$read_pfn` is the test file in `testpro:awt` to download, `$rse` is
the RSE name, and `$fn` is temporary test file created locally by the 
jobscript.

All of the verbose outputs of these commands are logged to the jobscript
logfile, which is available in full by looking at the Landscape page for
each job. There is a link to the Landscape webserver's files for each job
on each job's page on the justIN dashboard.

At the end of the jobscript, it outputs a summary of the `xrdcp` and 
`rucio upload` commands executed, and then their outcomes for each RSE
tested from this job. These final outputs are visible in the short Jobscript
Log section at the foot of each job's page in the justIN dashboard.

When the jobscript log is uploaded to the justIn allocator, it is parsed to
extract the test outcomes. These are stored in the justIN database and
visible on the pages for each site and storage accessible from the lists
of [all sites](https://justin.dune.hep.ac.uk/dashboard/?method=list-sites),
[all storages](https://justin.dune.hep.ac.uk/dashboard/?method=list-storages),
and on the 
[AWT results page](https://justin.dune.hep.ac.uk/dashboard/?method=awt-results).

Each result is also logged as a justIN event, associated with the job, RSE
and site. There are links to lists of these events from the above pages for
each site and storage, which can be used to view the history of the tests.

