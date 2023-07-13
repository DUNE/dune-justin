# justIN Job Factory

The justIN Job Factory agent creates and submits wrapper jobs to HTCondor, 
which are 
each assigned to a specific execution site. It uses a mixture of matching 
successes, the outcome of test matches against the [justIN 
database](database.md), and site limits set in the database to determine 
how many wrapper jobs to submit and have waiting at each site.

Once a wrapper job lands on a worker node, it contacts the 
[allocator service](services.allocator.md) which
determines which unallocated files from one stage best match that 
worker node.

