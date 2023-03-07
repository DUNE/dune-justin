# Automated Workflow Tests

The Automated Workflow Tests (AWT) test the reading and writing to storages
from jobs, in the environment seen by user jobscripts. 

The 
[AWT results page](https://justin.dune.hep.ac.uk/dashboard/?method=awt-results)
shows site vs storage results for the download and upload tests run in jobs
at each site. The text on the page explains how red, green and orange
colours show whether the tests were successful for each combination of site
and storage. The "Last AWT job" column shows how long ago an AWT job ran
at each site and reported results, and this tests whether the sites are
accessilble to justIN jobs.

Generic jobs are tagged for AWT and targetted at each known 
[DUNE site](https://justin.dune.hep.ac.uk/dashboard/?method=list-sites),
whether it is enabled for user jobs or not.

The 
[AWT Request](https://justin.dune.hep.ac.uk/dashboard/?method=show-request&request_id=1)
is used to manage the jobs. It uses input files with the metadata query
`rucio-dataset testpro:awt` to find files in the testpro:awt Rucio dataset. 
The [justIN finder agent](/docs/agents.finder.md) looks for new files in
that dataset every two hours and caches the new file's replicas at that point.
This means that if a new file is added to the dataset, it should already be
replicated to the desired RSEs before it is added the testpro:awt dataset.
When adding a new RSE, a rule for it needs to be added to the testpro:awt
dataset. 

When an AWT-tagged generic job starts at a site, it contacts the 
[justIN allocator](/docs/services.allocator.md) and requests a jobscript
to execute in the normal way. The allocator recognises that the job is
tagged for AWT and returns an additional list of RSEs to be tested.

The jobscript is taken from the only stage of the AWT request and visible at
the foot of 
[that stage's page](https://justin.dune.hep.ac.uk/dashboard/?method=show-stage&request_id=1&stage_id=1).


