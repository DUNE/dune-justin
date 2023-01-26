##  Generic jobs

justIn's generic jobs are extensions of the jobsub/glideInWMS jobs
developed at Fermilab and inherit their properties. There is a one to one
mapping between an instance of a generic job in justIn and the
corresponding jobsub job. Consequently justIn uses jobsub style string IDs
when referring to jobs in log files, the Dashboard, environment variables
exposed to user scripts etc, and these take the form 
NNNNNN.N@jobsubNN.fnal.gov where N are integers.

Within justIn, a generic job is in one of several allocation
states given here:

- **submitted** - the job has been submitted by the 
  [Generic Job Factory](job-factory.md) but not yet allocated a request/stage
- **started** - the job has succesfully been allocated a stage within a 
  request to work on by the [allocator service](workflow-allocator.md) and 
  the supplied bootstrap script should be running
- **processing** - the bootstrap script has successfully been allocated at 
  least one input file to process by the allocator service.
- **outputting** - the bootstrap script has finished and the generic job has
  reported to the allocator service the list of
  input files it processed and the names of the output files it intends to
  register with MetaCat and Rucio and to upload 
- **finished** - the generic job has successfully registered and uploaded
  the output files and confirmed this to the allocator service.
- **notused** - the generic job was unable to find a suitable request/stage
  to work on and exited.
- **aborted** - the generic job failed in some way and reported this to the
  allocator service.
- **stalled** - the [Finder](finder.md) agent has identified that the job 
  stopped sending regular heartbeats and has marked it as stalled. This may
  be because the job was killed by a local batch system for exceeding limits
  on memory usage etc.
