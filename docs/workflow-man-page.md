## workflow command man page
This man page is distributed along with the 
[workflow command](workflow-command.md) itself.
```
WORKFLOW(2022)                                                  WORKFLOW(2022)



NAME
       workflow - Workflow System utility command

SYNOPSIS
       workflow subcommand [options]

DESCRIPTION
       workflow  is  a  command-line  utility  for  managing requests, stages,
       files, and replicas in the Workflow System Database (WFDB).


GENERAL OPTIONS
       -h, --help
              Show help message and exit


       -v, --verbose
              Turn on verbose logging of the communication with the WFDB  ser-
              vice.


       --url URL
              Use  an  alternative  Worklow  Service, rather than https://wfs-
              pro.dune.hep.ac.uk/wfdb-cgi This option is  only  needed  during
              development and testing.


SUBCOMMANDS
       version
              Output the version number of the workflow command.


       create-request   [--name   NAME]   [--mql   QUERY|--monte-carlo  COUNT]
              [--refind-start-date  YYYYMMDD]  [--refind-duration-days   DAYS]
              [--refind-interval-hours HOURS]
              Create a new, empty request in the database, optionally with the
              given human-readable name and either a  MetaCat  Query  Language
              expression  or  the count of the number of Monte Carlo instances
              to run. If a name is not given, a name based on a  timestamp  is
              created.  Requests are created in the state "draft" and the com-
              mand returns the new request's ID number.  Once the  request  is
              in  the  running  state,  the  Workflow  System will use the MQL
              expression to find the list of  input  files  from  MetaCat.  If
              --refind-interval-hours  is  given, the MQL query will be resub-
              mitted at that interval to add any new matching files  from  the
              start of the day given by --refind-start-date (default: today in
              UTC) for the number  of  days  given  by  --refind-duration-days
              (default: 1).


       show-requests [--request-id ID]
              Show  details of all requests or optionally of a single request.
              Each line of the output gives the request  ID,  state,  creation
              time, name, and MetaCat query of one request.


       submit-request --request-id ID
              Currently not used.  Changes the state of the given request from
              "draft" to "submitted". In the future, this will allow automated
              sanity  checking  and prioritisation of requests. For very large
              requests it may give an opportunity for manual approval  by  the
              operations team.


       start-request --request-id ID
              Starts a request in the "draft" or "submitted" state or restarts
              a request in the "paused" stated, and changes its state to "run-
              ning".


       pause-request --request-id ID
              Changes  the  state of the given request to "paused". This state
              temporarily excludes a  request  from  the  workflow  allocation
              process.


       finish-request --request-id ID
              Changes the state of the given request to "finished". This state
              excludes a request from the workflow allocation process.


       create-stage --request-id ID --stage-id ID --file FILENAME [--wall-sec-
              onds  N]  [--rss-mb  N]  [--processors  N] [--max-distance DIST]
              [--output-pattern SCOPE:DATASET:PATTERN] [--output-pattern-next-
              stage SCOPE:DATASET:PATTERN] [--output-rse NAME]
              Creates  a  new  stage  for  the given request ID with the given
              stage ID. Stages must be numbered consecutively from 1, and each
              request  must  have  at  least one stage. Each stage must have a
              boostrap shell script associated with it, given  by  the  --file
              option  which  will  be  executed on worker nodes to process its
              files.

              If the maximum wallclock time needed is not given by --wall-sec-
              onds  then  the default of 80000 seconds is used. If the maximum
              amount of resident memory needed is not given by  --rss-mb  then
              the  default of 2048MiB is used. The resident memory corresponds
              to the physical memory  managed  by  HTCondor's  ResidentSetSize
              value.

              If the script can make use of multiple processors then --proces-
              sors can be used to give the number needed, with a default of  1
              if not given.

              By default, input files will only be allocated to a script which
              are on storages at the  same  site  (distance=0).  This  can  be
              changed  by  setting --max-distance DIST to allow input files to
              be allocated on storages at greater distances, up to a value  of
              100 which represents maximally remote storages.

              If one or more options --output-pattern SCOPE:DATASET:PATTERN is
              given then the generic job will look for files  created  by  the
              script  which match the pattern given as PATTERN. The pattern is
              a Bash shell pattern using *, ? and [...] expressions.  See  the
              bash(1)  Pattern  Matching section for details. Any output files
              found by this matching will be uploaded and  registered  by  the
              generic  job in the Rucio dataset given by SCOPE:DATASET, with a
              DID composed of the scope given and the found filename. Further-
              more, if the found files have a corresponding JSON metadata file
              with the same name but  with  ".json"  appended,  that  will  be
              recorded for that file in MetaCat.

              Alternatively  --output-pattern-next-stage SCOPE:DATASET:PATTERN
              can be given in which the output file will also be registered in
              the  Workflow Database as an unprocessed input file for the next
              stage and available for allocation to instances of that  stage's
              script.

              If  one or more options --output-rse NAME is given, then the RSE
              used for uploads of output files will be chosen from  that  list
              of  RSEs, with preference given to RSEs which are closer in dis-
              tance. If this option is not used, or none of the given RSEs are
              available,  then  the default algorithm for choosing the closest
              available RSE is used.


       quick-request   [--name   NAME]   [--mql   QUERY|--monte-carlo   COUNT]
              [--refind-start-date   YYYYMMDD]  [--refind-duration-days  DAYS]
              [--refind-interval-hours HOURS] --file FILENAME  [--wall-seconds
              N]  [--rss-mb  N] [--processors N] [--max-distance DIST] [--out-
              put-pattern SCOPE:DATASET:PATTERN] --output-rse NAME
              Combines the create-request, create-stage and start-request sub-
              commands  into  a  single  operation,  for use with single-stage
              requests.


       show-stages --request-id ID [--stage-id ID]
              Shows details of all stages of the given request  or  optionally
              of a single stage of that request. Each line of the output gives
              the request ID, stage ID,, min processors, max  processors,  max
              wallclock seconds, max RSS bytes, and the max distance value.


       show-bootstrap --request-id ID --stage-id ID
              Show  the  bootstrap  script of the given stage within the given
              request.


       show-stage-outputs --request-id ID --stage-id ID
              Shows the datasets to be assigned and the patterns used to  find
              output  files  of the given stage within the given request. Each
              line of the response consists of "(next)" or "(  )" depending on
              whether  the  files  are  passed  to  the  next stage within the
              request, and then the dataset, scope, and  files  pattern  them-
              selves.


       show-storages [--rse-name NAME]
              Shows  information  about  Rucio  Storage Elements cached in the
              Workflow Database, optionally limiting output to  a  single  RSE
              using its name. Each line of the output consists of the RSE name
              followed by the occupancy fraction obtained from  Rucio  in  the
              range 0.0 to 1.0, and the Read, Write and Delete availability of
              the RSE from Rucio, and whether the RSE will be included in  the
              default list for output files.


       show-sites-storages [--site-name NAME] [--rse-name NAME]
              Shows  information about the distances of Rucio storage elements
              relative to sites, optionally limited to the given  site  and/or
              RSE.  Each line of the output gives the site name, RSE name, and
              then their relative distance between 0 (same site) and 100 (max-
              imally remote).


       add-file --request-id ID [--stage-id ID] --file-did DID --rse-name NAME
              --pfn URL
              Adds one file to the list of files to be processed in  a  stage,
              with  the given Rucio file Data Identifier (DID).  Normally this
              should only be done for the first stage, which is  the  default.
              Files are created in the "unallocated" state, ready for process-
              ing. Exactly RSE which has a replica of the file must  be  given
              along  with one PFN to access the replica on that RSE. This sub-
              command is only intended for testing,  as  normally  the  Finder
              agent builds the lists of files and replicas for the first stage
              of a request using MetaCat and Rucio.


       show-files [--request-id ID] [--stage-id ID] [--file-did DID]
              Shows files information cached in the Workflow Database,  either
              limited  by  request  ID  and  stage ID or by file DID. For each
              file, the request ID, stage ID, file state,  and  file  DID  are
              shown. The file state is one of "finding", "unallocated", "allo-
              cated", or "processed". Files wait in the  "unallocated"  state,
              are  then  allocated to an instance of the stage's script by the
              Workflow Allocator, and then either return to  "unallocated"  or
              move  to  "processed" depending on whether the script is able to
              process them correctly.


       show-replicas [--request-id ID] [--stage-id ID] [--file-did DID]
              Shows file and replica information  in  the  Workflow  Database,
              either  limited  by  request ID and stage ID or by file DID. For
              each replica of each file, the request ID, stage ID, file state,
              RSE name, and file DID are shown.


       show-jobs  --jobsub-id  ID  |  --request-id ID [--stage-id ID] [--state
              STATE]
              Show jobs identified by Jobsub ID or Request ID (and  optionally
              Stage  ID).  Job  state  can also be given to further filter the
              jobs listed. For each job, the Jobsub ID, Request ID, Stage  ID,
              State, and creation time are shown.


BOOTSTRAP SCRIPTS
       The  bootstrap scripts supplied when creating a stage are shell scripts
       which the generic jobs execute on the  worker  nodes  matched  to  that
       stage.   They  are  started  in  an empty workspace directory.  Several
       environment variables are made available to the scripts,  all  prefixed
       with  WFS_,  including  $WFS_REQUEST_ID,  $WFS_STAGE_ID and $WFS_COOKIE
       which allows the bootstrap script to authenticate to the Workflow Allo-
       cator. $WFS_PATH is used to reference files and scripts provided by the
       Workflow System.

       To  get  the  details  of  an  input  file  to  work  on,  the  command
       $WFS_PATH/wfs-get-file  is executed by the bootstrap script.  This pro-
       duces a single line of output with the Rucio DID of  the  chosen  file,
       its  PFN on the optimal RSE, and the name of that RSE, all separated by
       spaces. This code fragment shows how the DID, PFN and RSE  can  be  put
       into shell variables:

         did_pfn_rse=`$WFS_PATH/wfs-get-file`
         did=`echo $did_pfn_rse | cut -f1 -d' '`
         pfn=`echo $did_pfn_rse | cut -f2 -d' '`
         rse=`echo $did_pfn_rse | cut -f3 -d' '`

       If  no file is available to be processed, then wfs-get-file produces no
       output to stdout, which should also be checked for.  wfs-get-file  logs
       errors to stderr.

       wfs-get-file can be called multiple times to process more than one file
       in the same bootstrap script. This can be done  all  at  the  start  or
       repeatedly  during  the  lifetime  of the job. wfs-get-file is itself a
       simple wrapper around the curl command and it would also be possible to
       access  the Workflow Allocator's REST API directly from an application.

       Each file returned by wfs-get-file is marked as allocated and will  not
       be  processed by any other jobs. When the bootstrap script finishes, it
       must leave files with lists of the processed and unprocessed  files  in
       its workspace directory. These lists are sent to the Workflow Allocator
       by the generic job, which either marks input files  as  being  success-
       fully  processed or resets their state to unallocated, ready for match-
       ing by another job.

       Files can be referred to either by DID or PFN, one  per  line,  in  the
       appropriate list file:
         wfs-processed-dids.txt
         wfs-processed-pfns.txt
         wfs-unprocessed-dids.txt
         wfs-unprocessed-pfns.txt

       It  is  not  necessary  to  create  list files which would otherwise be
       empty. You can use a mix of DIDs and PFNs, as long as each  appears  in
       the correct list file.

       Output  files  which  are  to be uploaded with Rucio by the generic job
       must be created in the bootstrap's workspace directory and  have  file-
       names  matching the patterns given by --output-pattern or --output-pat-
       tern-next-stage when the stage  was  created.  The  suffixed  .json  is
       appended to find the corresponding metadata files for MetaCat.


REQUEST PROCESSING
       Once  a  request enters the running state, it is processed by the Work-
       flow System's Finder agent. Usually this is just done once, but it  can
       be  repeated if the --refind-interval-hours option is given when creat-
       ing the request. When the request is processed,  the  Finder  uses  the
       requests's MQL expression to create a list of input files for the first
       stage. Work is only assigned to jobs when a matching file is found  and
       so these lists of files are essential.

       In  most  cases,  the MQL query is a MetaCat Query Language expression,
       which the Finder sends to the MetaCat service to get a list of matching
       file  DIDs.   However,  if  the  query  is  of  the form "rucio-dataset
       SCOPE:NAME" then the query is sent directly to Rucio to get the list of
       file DIDs contained in the given Rucio dataset. Finally if the --monte-
       carlo COUNT option is used when creating the request, then  an  MQL  of
       the  form  "monte-carlo COUNT" is stored. This causes the Finder itself
       to create a series of COUNT placeholder files which can be used to keep
       track  of Monte Carlo processing without a distinct input file for each
       of the COUNT jobs.  Each of these placeholder files has a  DID  of  the
       form  monte-carlo-REQUEST_ID-NUMBER  where  NUMBER is in the range 1 to
       COUNT, and REQUEST_ID is the assigned request ID number.


FILES
       An X.509 user proxy file is currently needed to  contact  the  Workflow
       Service,    which    is    either    given   by   $X509_USER_PROXY   or
       /tmp/x509up_uUSERID where USERID is the numeric Unix user id, given  by
       id -u


AUTHOR
       Andrew McNab <Andrew.McNab@cern.ch>


SEE ALSO
       bash(1)



WFS Manual                         workflow                     WORKFLOW(2022)
```
