# Automated Workflow Tests

justIN's Automated Workflow Tests (AWT) test the reading and writing to 
storages from jobs, in the environment seen by user jobscripts. 

The 
[AWT results page](https://dunejustin.fnal.gov/dashboard/?method=awt-results)
shows site vs storage results for the download and upload tests run in jobs
at each site. The text on the page explains how red, green and orange
colours show whether the tests were successful for each combination of site
and storage. The "Last AWT job" column shows how long ago an AWT job ran
at each site and reported results, and so tests whether the sites are
accessilble to justIN jobs. It also has a link to that job's page on the 
justIN dashboard. The "Last OSG time" column shows how long ago each site
was seen in the OSG pilot factory configurations, fetched by the 
[justIN info collector agent](/docs/agents.info_collector.md) from the 
[OSG pilot factory GitHub repo](https://github.com/opensciencegrid/osg-gfactory).

Wrapper jobs are tagged for AWT and targetted at each known 
[DUNE site](https://dunejustin.fnal.gov/dashboard/?method=list-sites),
whether it is enabled for user jobs or not.

The 
[AWT Workflow](https://dunejustin.fnal.gov/dashboard/?method=show-workflow&workflow_id=1)
is used to manage the jobs. It uses the metadata query
`rucio-dataset testpro:awt` to find files in the testpro:awt Rucio dataset. 
The [justIN finder agent](/docs/agents.finder.md) looks for new files in
that dataset every two hours. At the same time, existing files in the 
testpro:awt dataset are reset to the finding state. The finder agent then
looks for the replicas of the new and existing files, updating the PFNs
of the already cached replicas and adding new replicas as appropriate.

This means that new rules can be added to the testpro:awt dataset for new
RSEs and the Rucio configuration of the root protocol of the RSEs can be 
changed. In either case, the changes will be reflected in new AWT tests
within about two hours.

When an AWT-tagged wrapper job starts at a site, it contacts the 
[justIN allocator](/docs/services.allocator.md) and workflows a jobscript
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

The jobscript is taken from the single stage of the AWT workflow and is 
visible at the foot of 
[that stage's page](https://dunejustin.fnal.gov/dashboard/?method=show-stage&workflow_id=1&stage_id=1).

The production VOMS proxy normally used by the wrapper job for file uploads
is made available to the AWT jobscript at `$JUSTIN_PATH/awt-proxy.pem` and
this is currently used for both read and write tests. 

    voms-proxy-info --all --file $JUSTIN_PATH/awt-proxy.pem

is run by jobscript to show exactly what proxy is being used.

The jobscript loops through `$JUSTIN_PATH/justin-awt-rse-list.txt` doing

    xrdcp --force --nopbar --verbose "$read_pfn" "downloaded.txt"

and 

    rucio --verbose upload --rse $rse_name --protocol $write_protocol \
          --scope testpro --lifetime 86400 --name $fn $fn

where `$read_pfn` is the test file in `testpro:awt` to download, `$rse` is
the RSE name, and `$fn` is temporary test file created locally by the 
jobscript.

All of the verbose outputs of these commands are logged to the jobscript
logfile, which is available in full by looking at the job wrapper logs page 
for each job. There is a link to the wrapper job logs for each job
on each job's page on the justIN dashboard.

At the end of the jobscript, it outputs a summary of the `xrdcp` and 
`rucio upload` commands executed, and then their outcomes for each RSE
tested from this job. These final outputs are visible in the short Jobscript
Log section at the foot of each job's page in the justIN dashboard.

When the jobscript log is uploaded to the justIN allocator, it is parsed to
extract the test outcomes. These are stored in the justIN database and
visible on the pages for each site and storage accessible from the lists
of [all sites](https://dunejustin.fnal.gov/dashboard/?method=list-sites),
[all storages](https://dunejustin.fnal.gov/dashboard/?method=list-storages),
and on the 
[AWT results page](https://dunejustin.fnal.gov/dashboard/?method=awt-results).

Each result is also logged as a justIN event, associated with the job, RSE
and site. There are links to lists of these events from the above pages for
each site and storage, which can be used to view the history of the tests.

For sites with at least one entry supporting GPUs, a GPU AWT jobs is also 
submitted each time which requires at least one GPU. If this job runs
successfully, then the site's last successful GPU job time is updated. This
is visible on the per-site pages and the main AWT results page.
