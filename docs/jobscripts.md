# Jobscripts

The jobscripts supplied when creating a stage are shell scripts 
which the wrapper jobs execute for the user, on the worker nodes matched 
to that stage.  

They are started in an empty workspace directory.  Several environment 
variables are made available to the scripts, all prefixed with JUSTIN_, 
including $JUSTIN_WORKFLOW_ID, $JUSTIN_STAGE_ID and $JUSTIN_SECRET which allows
the jobscript to authenticate to the 
[allocator service](services.allocator.md). $JUSTIN_PATH is 
used to reference files and scripts provided by justIN.

To get the details of an input file to work on, the command 
$JUSTIN_PATH/justin-get-file is executed by the jobscript.  This produces 
a single line of output with the Rucio DID of the chosen file, its PFN on 
the optimal RSE, and the name of that RSE, all separated by spaces. This 
code fragment shows how the DID, PFN and RSE can be put into shell 
variables:

    did_pfn_rse=`$JUSTIN_PATH/justin-get-file`
    did=`echo $did_pfn_rse | cut -f1 -d' '`
    pfn=`echo $did_pfn_rse | cut -f2 -d' '`
    rse=`echo $did_pfn_rse | cut -f3 -d' '`

If no file is available to be processed, then justin-get-file produces no 
output to stdout, which should also be checked for.  justin-get-file logs 
errors to stderr.

justin-get-file can be called multiple times to process more than one file in 
the same jobscript. This can be done all at the start or repeatedly 
during the lifetime of the job. justin-get-file is itself a simple wrapper 
around the curl command and it would also be possible to access the 
allocator service's REST API directly from an application.

Each file returned by justin-get-file is marked as allocated and will not be 
processed by any other jobs. When the jobscript finishes, it must 
leave files with lists of the files it processed in its 
workspace directory. These lists are sent to the allocator service by the 
wrapper job which marks those input files as being successfully 
processed. Any allocated files which are not listed are treated as
unprocessed, and the allocator service resets their state to unallocated, 
ready for matching by another job.

Files can be referred to either by DID or PFN, one  per  line,  in  the
appropriate list file:

    justin-processed-dids.txt
    justin-processed-pfns.txt


It is not necessary to create list files which would otherwise be empty. 
You can refer to each processed file either by its DID or PFN (or both!) as
long as they are put in the correct list file. 

Output files which are to be uploaded with Rucio by the wrapper job must 
be created in the jobscript's workspace directory and have filenames 
matching the patterns given by --output-pattern or 
--output-pattern-next-stage when the stage was created.  The suffix 
.json is appended to find the corresponding metadata files for MetaCat.
