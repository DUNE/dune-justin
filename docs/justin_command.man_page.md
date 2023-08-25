# justin command man page
This man page is distributed along with the 
[justin command](justin_command.md) itself.

    JUSTIN(2023)							  JUSTIN(2023)
    
    NAME
           justin - justIN workflow system utility command
    
    SYNOPSIS
           justin subcommand [options]
    
    DESCRIPTION
           justin is a command-line utility for managing workflows, stages, files,
           and replicas in the justIN workflow system.
    
    
    GENERAL OPTIONS
           -h, --help
    	      Show help message and exit
    
    
           -v, --verbose
    	      Turn on verbose logging of the communication with justIN
    	      service.
    
    
           --url URL
    	      Use an alternative justIN service, rather than https://justin-
    	      ui-pro.dune.hep.ac.uk/api/commands This option is only needed
    	      during development and testing.
    
    
    SUBCOMMANDS
           version
    	      Output the version number of the justin command.
    
    
           time   Contact justIN to get the current time as a string. This can be
    	      used to check that the client is installed correctly and that
    	      the user is properly registered in justIN.
    
    
           whoami
    	      Displays information about the current user identity and
    	      session.
    
    
           create-workflow [--description DESC] [--mql QUERY|--monte-carlo COUNT]
    	      [--scope SCOPE]
    	      Create a new, empty workflow in the database, optionally with
    	      the given short, human-readable description and either a MetaCat
    	      Query Language expression or the count of the number of Monte
    	      Carlo instances to run.
    
    	      --scope SCOPE specifies the Rucio scope used for any output
    	      files to be registered with Rucio and uploaded to Rucio-managed
    	      storage.
    
    	      Workflows are created in the state "draft" and the command
    	      returns the new workflow's ID number.  Once the workflow is in
    	      the running state, justIN will use the MQL expression to find
    	      the list of input files from MetaCat.
    
           show-workflows [--workflow-id ID]
    	      Show details of all workflows or optionally of a single
    	      workflow. Each line of the output gives the workflow ID, state,
    	      creation time, description, and MetaCat query of one workflow.
    
    
           submit-workflow --workflow-id ID
    	      Changes the state of the given workflow from "draft" to
    	      "submitted". The justIN Finder agent will automatically set the
    	      workflow to running after any necessary initialisation.
    
    
           restart-workflow --workflow-id ID
    	      Restarts a workflow in the "paused" stated, and changes its
    	      state to "running".
    
    
           pause-workflow --workflow-id ID
    	      Changes the state of the given running workflow to "paused".
    	      This state temporarily excludes a workflow from the workflow
    	      allocation process.
    
    
           finish-workflow --workflow-id ID
    	      Changes the state of the given running workflow to "finished".
    	      This state excludes a workflow from the workflow allocation
    	      process.
    
    
           create-stage --workflow-id ID --stage-id ID  --jobscript
    	      FILENAME|--jobscript-id JSID [--wall-seconds N] [--rss-mb N]
    	      [--processors N] [--max-distance DIST] [--output-pattern
    	      PATTERN:DESTINATION] [--output-pattern-next-stage
    	      PATTERN:DATASET] [--output-rse NAME] [--lifetime-days DAYS]
    	      [--env NAME=VALUE] [--classad NAME=VALUE]
    	      Creates a new stage for the given workflow ID with the given
    	      stage ID. Stages must be numbered consecutively from 1, and each
    	      workflow must have at least one stage.
    
    	      Each stage must have a jobscript shell script associated with
    	      it, given by the --jobscript or --jobscript-id options.  Either
    	      the full, local path to the jobscript file is given, or the
    	      jobscript is taken from justIN's Jobscripts Library using a JSID
    	      jobscript identifier.  The JSID is in the form SCOPE:NAME or
    	      USER:NAME, where USER includes an '@' character. In either case,
    	      a copy of the current text of the jobscript is cached in the
    	      stage definition and executed on worker nodes to process the
    	      stage's files.
    
    	      If the maximum wallclock time needed is not given by
    	      --wall-seconds then the default of 80000 seconds is used. If the
    	      maximum amount of resident memory needed is not given by
    	      --rss-mb then the default of 2000MiB is used. The resident
    	      memory corresponds to the physical memory managed by HTCondor's
    	      ResidentSetSize value.
    
    	      If the script can make use of multiple processors then
    	      --processors can be used to give the number needed, with a
    	      default of 1 if not given.
    
    	      By default, input files will only be allocated to a script which
    	      are on storages at the same site (distance=0). This can be
    	      changed by setting --max-distance DIST to allow input files to
    	      be allocated on storages at greater distances, up to a value of
    	      100 which represents maximally remote storages.
    
    	      If one or more options --output-pattern PATTERN:DESTINATION is
    	      given then the wrapper job will look for files created by the
    	      script which match the pattern given as PATTERN. The pattern is
    	      a Bash shell pattern using *, ? and [...] expressions. See the
    	      bash(1) Pattern Matching section for details.  The DESTINATION
    	      component has any of the variables $JUSTIN_SCOPE,
    	      $JUSTIN_WORKFLOW_ID, or $JUSTIN_STAGE_ID replaced. The form
    	      ${JUSTIN_SCOPE} etc may also be used.  If the given DESTINATION
    	      starts with https:// then the matching output files will be
    	      uploaded to WebDAV scratch space, such as dCache at Fermilab.
    	      The DESTINATION must be the URL of a directory accessible via
    	      WebDAV, and given with or without a trailing slash. Nested
    	      subdirectories for workflow ID and stage ID will be added, and
    	      resulting output files placed there. The user's token from the
    	      justIN dashboard is used for the upload.	If an https:// URL is
    	      not given, DESTINATION is interpreted as a Rucio dataset minus
    	      the scope component. The overall scope of the workflow is used
    	      and the output files are uploaded with Rucio and registered in
    	      that dataset. If the dataset does not already exist then it will
    	      be created when the workflow changes state from submitted to
    	      running and if the --lifetime-days option is given, then a rule
    	      for the new dataset will be created with that lifetime rather
    	      than the default 1 day.  Furthermore, files for Rucio-managed
    	      storage must have a corresponding JSON metadata file with the
    	      same name but with ".json" appended, that will be recorded for
    	      that file in MetaCat.
    
    	      Alternatively --output-pattern-next-stage PATTERN:DATASET can be
    	      given in which case the output file will be uploaded to Rucio-
    	      managed storage and will also be registered in the justIN
    	      Database as an unprocessed input file for the next stage and
    	      available for allocation to instances of that stage's script.
    
    	      --lifetime-days DAYS sets the Rucio rule lifetime when creating
    	      a new dataset, for all output files that are uploaded in the
    	      given stage.  The lifetime defaults to 1 day if not specified.
    
    	      If one or more options --output-rse NAME is given, then the RSE
    	      used for uploads of output files will be chosen from that list
    	      of RSEs, with preference given to RSEs which are closer in
    	      distance. If this option is not used, or none of the given RSEs
    	      are available, then the default algorithm for choosing the
    	      closest available RSE is used.
    
    	      --env NAME=VALUE can be used one or more times to set
    	      environment variables when the stage's jobscript is executed.
    
    	      --classad NAME=VALUE can be used one or more times to add
    	      ClassAds to the jobs submitted for this stage.
    
    
           simple-workflow [--description DESC] [--mql QUERY|--monte-carlo COUNT]
    	      [--scope SCOPE] --jobscript FILENAME|--jobscript-id JSID
    	      [--wall-seconds N] [--rss-mb N] [--processors N] [--max-distance
    	      DIST] [--output-pattern PATTERN:DESTINATION] [--output-rse NAME]
    	      [--lifetime-days DAYS] [--env NAME=VALUE] [--classad NAME=VALUE]
    	      Combines the create-workflow, create-stage and submit-workflow
    	      subcommands into a single operation, for use with single-stage
    	      workflows. The options are repeated from the first two
    	      subcommands and are described in their respective sections
    	      above.
    
    
           show-stages --workflow-id ID [--stage-id ID]
    	      Shows details of all stages of the given workflow or optionally
    	      of a single stage of that workflow. Each line of the output
    	      gives the workflow ID, stage ID,, min processors, max
    	      processors, max wallclock seconds, max RSS bytes, and the max
    	      distance value.
    
    
           create-jobscript [--description DESC] [--scope SCOPE] --name NAME
    	      --jobscript FILENAME
    	      Creates a named jobscript in the Jobscripts Library, with an
    	      optional description. The jobscript is created with the
    	      specified scope if one is given. Otherwise the jobscript is
    	      created under your user name. The jobscript identifier is
    	      returned on success, in the form SCOPE:NAME or USER:NAME.
    	      Jobscript names must be unique for each scope or user name. If a
    	      jobscript already exists for the given scope or user name it is
    	      overwritten.
    
           show-jobscript --jobscript-id JSID
           show-jobscript --workflow-id ID --stage-id ID
    	      Show a jobscript, referenced either by a jobscript identifier or
    	      by workflow and stage. If an identifier is given, the jobscript
    	      is taken from the Jobscripts Library. The JSID identifier
    	      consists of USER:NAME or SCOPE:NAME, where NAME is the jobscript
    	      name, USER is the user name of any user and contains an '@'
    	      character, and SCOPE is a Rucio scope name known to justIN.
    	      Alternatively, if workflow and stage are given, then the
    	      jobscript cached for that workflow and stage is shown.
    
           show-stage-outputs --workflow-id ID --stage-id ID
    	      Shows the datasets to be assigned and the patterns used to find
    	      output files of the given stage within the given workflow. Each
    	      line of the response consists of "(next)" or "(  )" depending on
    	      whether the files are passed to the next stage within the
    	      workflow, and then the scope, files pattern, and destination.
    
    
           fail-files --workflow-id ID [--stage-id ID]
    	      Set all the files of the given workflow, and optionally stage,
    	      to the failed state when they are already in the finding,
    	      unallocated, allocated, or outputting state. Files in the
    	      processed, failed, or notfound states are unchanged. This allows
    	      workflows with a handful of pathological files to be terminated,
    	      as the Finder agent will see all the files are now in terminal
    	      states and mark the workflow as finished.
    
           show-files --workflow-id ID [--stage-id ID] [--file-did DID]
           show-files --mql QUERY
    	      Show up to 100 files either cached in the justIN Database and
    	      filtered by workflow ID and optionally by stage ID and/or file
    	      DID; or found by a query to MetaCat using the given MQL query.
    
           show-replicas --workflow-id ID [--stage-id ID] [--file-did DID]
           show-replicas --mql QUERY
    	      Show up to 100 replicas either cached in the justIN Database and
    	      filtered by workflow ID and optionally by stage ID and/or file
    	      DID; or found by a query to MetaCat using the given MQL query
    	      and looked up using Rucio.
    
           show-jobs --jobsub-id ID | --workflow-id ID [--stage-id ID] [--state
    	      STATE]
    	      Show jobs identified by Jobsub ID or Workflow ID (and optionally
    	      Stage ID). Job state can also be given to further filter the
    	      jobs listed. For each job, the Jobsub ID, Workflow ID, Stage ID,
    	      State, and creation time are shown.
    
    
    JOBSCRIPTS
           The user jobscripts supplied when creating a stage are shell scripts
           which the wrapper jobs execute on the worker nodes matched to that
           stage.  They are started in an empty workspace directory.  Several
           environment variables are made available to the scripts, all prefixed
           with JUSTIN_, including $JUSTIN_WORKFLOW_ID, $JUSTIN_STAGE_ID and
           $JUSTIN_SECRET which allows the jobscript to authenticate to justIN's
           allocator service. $JUSTIN_PATH is used to reference files and scripts
           provided by justIN.
    
           To get the details of an input file to work on, the command
           $JUSTIN_PATH/justin-get-file is executed by the jobscript.  This
           produces a single line of output with the Rucio DID of the chosen file,
           its PFN on the optimal RSE, and the name of that RSE, all separated by
           spaces. This code fragment shows how the DID, PFN and RSE can be put
           into shell variables:
    
    	 did_pfn_rse=`$JUSTIN_PATH/justin-get-file`
    	 did=`echo $did_pfn_rse | cut -f1 -d' '`
    	 pfn=`echo $did_pfn_rse | cut -f2 -d' '`
    	 rse=`echo $did_pfn_rse | cut -f3 -d' '`
    
           If no file is available to be processed, then justin-get-file produces
           no output to stdout, which should also be checked for. justin-get-file
           logs errors to stderr.
    
           justin-get-file can be called multiple times to process more than one
           file in the same jobscript. This can be done all at the start or
           repeatedly during the lifetime of the job. justin-get-file is itself a
           simple wrapper around the curl command and it would also be possible to
           access the justIN allocator service's REST API directly from an
           application.
    
           Each file returned by justin-get-file is marked as allocated and will
           not be processed by any other jobs. When the jobscript finishes, it
           must leave files with lists of the processed files in its workspace
           directory. These lists are sent to the justIN allocator service by the
           wrapper job, which either marks input files as being successfully
           processed or resets their state to unallocated, ready for matching by
           another job.
    
           Files can be referred to either by DID or PFN, one per line, in the
           appropriate list file:
    	 justin-processed-dids.txt
    	 justin-processed-pfns.txt
    
           It is not necessary to create list files which would otherwise be
           empty. You can use a mix of DIDs and PFNs, as long as each appears in
           the correct list file. Any files not represented in either file will be
           treated as unprocessed and made available for other jobs to process.
    
           Output files which are to be uploaded with Rucio by the wrapper job
           must be created in the jobscript's workspace directory and have
           filenames matching the patterns given by --output-pattern or
           --output-pattern-next-stage when the stage was created. The suffixed
           .json is appended to find the corresponding metadata files for MetaCat.
    
    
    WORKFLOW PROCESSING
           Once a workflow enters the running state, it is processed by justIN's
           Finder agent to find its input files. The finder uses the workflows's
           MQL expression to create a list of input files for the first stage.
           Work is only assigned to jobs when a matching file is found and so
           these lists of files are essential.
    
           In most cases, the MQL query is a MetaCat Query Language expression,
           which the Finder sends to the MetaCat service to get a list of matching
           file DIDs.  However, if the query is of the form "rucio-dataset
           SCOPE:NAME" then the query is sent directly to Rucio to get the list of
           file DIDs contained in the given Rucio dataset. Finally if the
           --monte-carlo COUNT option is used when creating the workflow, then an
           MQL of the form "monte-carlo COUNT" is stored. This causes the Finder
           itself to create a series of COUNT placeholder files which can be used
           to keep track of Monte Carlo processing without a distinct input file
           for each of the COUNT jobs.  Each of these placeholder files has a DID
           of the form monte-carlo-WORKFLOW_ID-NUMBER where NUMBER is in the range
           1 to COUNT, and WORKFLOW_ID is the assigned workflow ID number.
    
    
    AUTHENTICATION AND AUTHORIZATION
           When first used on a given computer, the justin command contacts the
           central justIN services and obtains a session ID and secret which are
           placed in a temporary file. You will then be invited to visit a web
           page on the justIN dashboard which has instructions on how to authorize
           that session, using CILogon and your identity provider. Once
           authorized, you can use the justin command on that computer for 7 days,
           and then you will be invited to re-authorize it. You can have multiple
           computers at multiple sites authorized at the same time.
    
    
    ENVIRONMENT
           If set, the value of the environment variable JUSTIN_OPTIONS is
           prepended to the list of options after the justin subcommand.
    
    
    FILES
           A session file /var/tmp/justin.session.USERID is created by justin,
           where USERID is the numeric Unix user id, given by id -u
    
    
    AUTHOR
           Andrew McNab <Andrew.McNab@cern.ch>
    
    
    SEE ALSO
           bash(1)
    
    justIN Manual			    justin			  JUSTIN(2023)
