## Generic Job Factory

The Generic Job Factory agent creates and submits HTCondor jobs, which are 
each assigned to a specific execution site. It uses a mixture of matching 
successes, the outcome of test matches against the [Workflow 
Database](database.md), and site limits set in the database to determine 
how many generic jobs to submit and have waiting at each site.

Once a generic job lands on a worker node, it contacts the 
[Workflow Allocator](workflow-allocator.md) which
determines which unallocated files from one stage best match that 
worker node.

