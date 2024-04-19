## File processing lifecycle

Each justIN workflow has a list of input files to be processed, either real
files with replicas on storage or Monte Carlo counter files. The workflow
describes how to transform those input files into output files, and this
page explains the lifecycle of input and output files during that process.

### Input files

For real input files, the justIN Finder agent discovers input file DIDs from 
[MetaCat](https://metacat.readthedocs.io/en/latest/) 
with an MQL and stores them in the justIN database, associated with
the workflow in question, and in the finding state. 
The Finder agent then uses Rucio to look up the 
Physical File Names (PFNs) of the replicas of each file, and stores them
in the database, setting the files to the unallocated state.

For Monte Carlo counter files, the requested number of files and PFNs are
stored directly in the database with ascending numbers in their names.

As jobs start running on worker nodes for a particular workflow, the user's
jobscript runs the justin-get-file script which asks the justIN allocator
service for the DID and suggested PFN and RSE of a file to process. At this
point the input file's state is set to allocated.

The user's jobscript may execute justin-get-file multiple times and be
allocated multiple input files.

Eventually the jobscript finishes and returns an exit code. If the exit code
is non-zero, indicating an error, then all of the input files allocated to
this job are reset to unallocated or to failed (if the maximum number of
attempts are reason - by default 6.)

However, if the exit code is zero, then the files justin-processed-dids.txt
and/or justin-processed-pfns.txt produced by the jobscript are examined. The
files they list are treated as successfully processed and set to outputting
in the database, in preparation for the handling of the output files
created from them. Any allocated input files not included are reset to
unallocated or failed.

### Output files

Output files are specified using the list of one or more output patterns
included in the definition of the workflow/stage. These give the filesystem
wildcard patterns to use when looking for output files in the jobscript's
working directory, and associate each pattern with a Rucio dataset or scratch
upload location at Fermilab.

The wrapper job enters the outputting state by sending a record_results
message to the allocator service, and getting an OK back. This message
specifies the filenames of the output files to be uploaded, and they are all
added to the justIN database in the recorded state.

The wrapper job than goes through each output file, first registering it in 
MetaCat with dune.output_status=recorded, and then trying to upload it with
the Rucio upload client API. If the upload appears to succeed, then the
file's metadata in MetaCat is updated to set dune.output_status=uploaded.
Each MetaCat and Rucio operation is retried three times and three output
RSEs are tried (so nine attempts for Rucio in total). 

If MetaCat or Rucio
requests fail despite the retries, then the wrapper job gives up, sends an
abort message to the allocator, and stops. The allocator resets all of the 
input files to unallocated or failed.

If all output files are successfully registered in MetaCat and uploaded with
Rucio, then a confirm_results message is sent to the allocator. The
allocator updates all of the input files for that job in the outputting
state to processed, and updates all of its output files from the recorded
state to the finding or output state depending whether they are needed for
the next stage or not. 

If the allocator returns OK to the wrapper job, then wrapper job updates the
output files dune.output_status to confirmed in MetaCat. This is done one by
one, and so it is possible for this to fail halfway through.
