## Workflow Allocator

Once a generic job arrives at a worker node, it contacts the Workflow 
Allocator service which determines which unallocated file from one stage 
best matches that worker node. This matching includes the characteristics 
of the worker node job slot (memory, time limit etc), and whether the site 
is eligible to access a replica of that data file. The matching takes into 
account that some stage definitions allow access to remote input files 
anywhere on the grid, and others require files to be at a "nearby" site. 
Replicas are prioritized based on whether the worker node and replica are 
at the same site, "nearby", or elsewhere but still eligible.

The [bootstrap script](bootstrap-scripts.md) 
to run and details of the request and stage are 
returned to the generic job. The script can use these details to request a 
series of files to process with the application it invokes. Each input 
file successfully processed by the application is reported to the Workflow 
Allocator so that the input file’s status can be updated from Allocated to 
Processed. Unprocessed input files are returned to the unallocated state 
for processing in another job.

If the stage is not the final stage for that request, each output data 
file is also inserted into the list of files associated with the next 
stage for that request, in the unallocated state.
