# justin command man page
This man page is distributed along with the 
[justin command](justin_command.md) itself.

    JUSTIN(2024)							  JUSTIN(2024)
    
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
    
    
           --instance INST
    	      Use an alternative justIN service, rather than "fnal" instance
    	      at Fermilab.  This option is normally only needed during
    	      development and testing, and it may be convenient to set this
    	      option via $JUSTIN_OPTIONS described in Environment below.
    
    
           --url URL
    	      Use an alternative justIN service, rather than https://justin-
    	      ui-pro.dune.hep.ac.uk/api/commands This option is only needed
    	      during development and testing, and it may be convenient to set
    	      this option via $JUSTIN_OPTIONS described in Environment below.
    
    
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
    	      [--scope SCOPE] [--htcondor-group GROUP] [--refind-end-date
    	      YYYYMMDD] [--refind-interval-hours HOURS] [--workflow-id-file
    	      FILENAME]
    	      Create a new, empty workflow in the database, optionally with
    	      the given short, human-readable description and either a MetaCat
    	      Query Language expression or the count of the number of Monte
    	      Carlo instances to run.
    
    	      --scope SCOPE specifies the Rucio scope used for any output
    	      files to be registered with Rucio and uploaded to Rucio-managed
    	      storage. Scopes also determine which HTCondor group wrapper jobs
    	      are submitted to. If not given, the default scope usertests is
    	      used.
    
    	      --htcondor-group GROUP specifies the HTCondor group used when
    	      justIN submits jobs for this workflow. By default the scope's
    	      own default group is used. If this option is given, the first
    	      two parts of the selected group must match the first two parts
    	      of the scope's default group. For example, "group_dune" and
    	      "prod" if the scope's group is "group_dune.prod.mcsim"
    
    	      The options --refind-interval-hours (default 1) and
    	      --refind-end-date (default: today in UTC) can be used to cause
    	      MQL queries to be resubmitted at that interval to add any new
    	      matching files until the end of the given day.  At least one of
    	      these options must be given to trigger this behaviour and to
    	      ensure that files added close to the end of that day are still
    	      found, a final finding is done soon after the end time.
    
    	      Workflows are created in the state "draft" and the command
    	      returns the new workflow's ID number.  Once the workflow is in
    	      the running state, justIN will use the MQL expression to find
    	      the list of input files from MetaCat.
    
    	      The option --workflow-id-file FILENAME can be used to append a
    	      line with the ID of the new workflow to the given file.
    
    
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
    	      Changes the state of the given workflow from "draft",
    	      "submitted", or "running" to "finished". This state excludes a
    	      workflow from the allocation process.
    
    
           create-stage --workflow-id ID --stage-id ID  --jobscript
    	      FILENAME|--jobscript-git ORG/PATH:TAG [--wall-seconds N]
    	      [--rss-mib N] [--processors N] [--gpu] [--max-distance DIST]
    	      [--output-pattern PATTERN[:DESTINATION]]
    	      [--output-pattern-next-stage PATTERN[:DATASET]] [--output-rse
    	      NAME] [--output-rse-expression EXPRESSION] [--lifetime-days
    	      DAYS] [--env NAME=VALUE] [--classad NAME=VALUE] [--site
    	      SITENAME] [--image IMAGENAME]
    	      Creates a new stage for the given workflow ID with the given
    	      stage ID. Stages must be numbered consecutively from 1, and each
    	      workflow must have at least one stage.
    
    	      Each stage must have a jobscript shell script associated with
    	      it, given by the --jobscript or --jobscript-git options.	Either
    	      the full, local path to the jobscript file is given, or a
    	      reference to a tag or revison hash in GitHub is given.  A GitHub
    	      reference takes the form PATH:TAG where TAG is a git tag or SHA1
    	      revision hash, and PATH is the path to the jobscript file in
    	      GitHub's URL space, of the form
    	      ORGANISATION/REPO/DIRECTORIES/.../FILE.jobscript .  In both
    	      scenarios, a copy of the current text of the jobscript is cached
    	      in the stage definition and executed on worker nodes to process
    	      the stage's files.
    
    	      If the maximum wallclock time needed is not given by
    	      --wall-seconds then the default of 80000 seconds is used. The
    	      value used is available to jobscripts as $JUSTIN_WALL_SECONDS.
    	      If the maximum amount of resident memory needed is not given by
    	      --rss-mib then the default of 2000MiB is used. The resident
    	      memory corresponds to the physical memory managed by HTCondor's
    	      ResidentSetSize value and is available to jobscripts as
    	      $JUSTIN_RSS_MIB.	If the script can make use of multiple
    	      processors then --processors can be used to give the number
    	      needed, with a default of 1 if not given. The value used is
    	      available to jobscripts as $JUSTIN_PROCESSORS.  If given then
    	      --gpu will require that jobs for this stage have access to a
    	      GPU.
    
    	      By default, input files will only be allocated to a script which
    	      are on storages at the same site (distance=0). This can be
    	      changed by setting --max-distance DIST to allow input files to
    	      be allocated on storages at greater distances, up to a value of
    	      100 which represents maximally remote storages.
    
    	      If one or more options --output-pattern PATTERN[:DESTINATION] is
    	      given then the wrapper job will look for files created by the
    	      script which match the pattern given as PATTERN. The pattern is
    	      a Bash shell pattern using *, ? and [...] expressions. See the
    	      bash(1) Pattern Matching section for details.  If given, the
    	      DESTINATION component has any of the variables $JUSTIN_SCOPE,
    	      $JUSTIN_WORKFLOW_ID, or $JUSTIN_STAGE_ID replaced. The form
    	      ${JUSTIN_SCOPE} etc may also be used.  If the given DESTINATION
    	      starts with https:// then the matching output files will be
    	      uploaded to WebDAV scratch space, such as dCache at Fermilab.
    	      The DESTINATION must be the URL of a directory accessible via
    	      WebDAV, and given with or without a trailing slash. Nested
    	      subdirectories for workflow ID and stage ID will be added, and
    	      resulting output files placed there. The user's token from the
    	      justIN dashboard is used for the upload.	If an https:// URL is
    	      not given, DESTINATION is used when constructing the output
    	      dataset names. Datasets have the form DESTINATION-INST-wXsYpZ
    	      where INST is the instance, X is the workflow ID, Y is the
    	      stage, and Z is the output pattern ID number, starting from 1.
    	      If DESTINATION is not given then only the form wXsYpZ is used.
    
    	      Files for Rucio-managed storage may have a corresponding JSON
    	      metadata file with the same name but with ".json" appended, that
    	      will be recorded in the metadata for that file in MetaCat. If
    	      this is not given, then basic workflow metadata will still be
    	      recorded. If output files have parent-child relations, the
    	      parent output pattern must be given before the child so that the
    	      parents are known to MetaCat before the children declare them to
    	      be parents.
    
    	      Alternatively --output-pattern-next-stage PATTERN[:DESTINATION]
    	      can be given in which case the output file will be uploaded to
    	      Rucio-managed storage and will also be registered in the justIN
    	      Database as an unprocessed input file for the next stage and
    	      available for allocation to instances of that stage's script.
    
    	      --lifetime-days DAYS sets the Rucio rule lifetime when creating
    	      Rucio datasets for output files.	If any Rucio datasets are used
    	      for outputs, then this is option is required.
    
    	      If one or more options --output-rse NAME is given, then the RSE
    	      used for uploads of output files and log tgz files will be
    	      chosen from that list of RSEs, with preference given to RSEs
    	      which are closer in distance. If this option is not used, or
    	      none of the given RSEs are available, then the default algorithm
    	      for choosing the closest available RSE is used.
    
    	      If --output-rse-expression EXPRESSION is given, then it is used
    	      when creating rules for Rucio datasets for outputs, but not for
    	      the per-RSE datasets used to keep a copy of the output file on
    	      the RSE it is first uploaded to.
    
    	      --env NAME=VALUE can be used one or more times to set
    	      environment variables when the stage's jobscript is executed.
    
    	      --classad NAME=VALUE can be used one or more times to add
    	      ClassAds to the jobs submitted for this stage.
    
    	      --site SITENAME can be used to restrict jobs for this stage to a
    	      single site for testing.	If the site is not available, then no
    	      jobs will run.
    
    	      --image IMAGENAME can override the default Apptainer image
    	      (fnal-wn-sl7:latest) in which user jobscripts are run. The image
    	      tree must exist within
    	      /cvmfs/singularity.opensciencegrid.org/fermilab/ and if does not
    	      contain ":" then ":latest" is appended to the name given.
    
    
           simple-workflow [--description DESC] [--mql QUERY|--monte-carlo COUNT]
    	      [--scope SCOPE] [--htcondor-group GROUP] [--refind-end-date
    	      YYYYMMDD] [--refind-interval-hours HOURS] --jobscript
    	      FILENAME|--jobscript-git ORG/PATH:TAG [--wall-seconds N]
    	      [--rss-mib N] [--processors N] [--gpu] --max-distance DIST]
    	      [--output-pattern PATTERN[:DESTINATION]] [--output-rse NAME]
    	      [--output-rse-expression EXPRESSION] [--lifetime-days DAYS]
    	      [--env NAME=VALUE] [--classad NAME=VALUE] [--site SITENAME]
    	      [--image IMAGENAME] [--workflow-id-file FILENAME]
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
    
           show-jobscript --jobscript-git ORG/PATH:TAG
           show-jobscript --workflow-id ID --stage-id ID
    	      Show the given jobscript, either by GitHub reference or by
    	      workflow and stage.
    
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
    	      Show files either cached in the justIN Database and filtered by
    	      workflow ID and optionally by stage ID and/or file DID; or up to
    	      100 found by a query to MetaCat using the given MQL query.
    
           show-replicas --workflow-id ID [--stage-id ID] [--file-did DID]
           show-replicas --mql QUERY
    	      Show replicas either cached in the justIN Database and filtered
    	      by workflow ID and optionally by stage ID and/or file DID; or up
    	      to 100 found by a query to MetaCat using the given MQL query and
    	      looked up using Rucio.
    
           show-jobs --jobsub-id ID | --workflow-id ID [--stage-id ID] [--state
    	      STATE]
    	      Show jobs identified by Jobsub ID or Workflow ID (and optionally
    	      Stage ID). Job state can also be given to further filter the
    	      jobs listed. For each job, the Jobsub ID, Workflow ID, Stage ID,
    	      State, and creation time are shown.
    
           fetch-logs --jobsub-id ID [--unpack]
    	      Download and optionally unpack the logs.tgz file for a given
    	      job. The file is placed in the current directory and if the
    	      --unpack option is given, it will be unpacked into a directory
    	      named for the job.  This subcommand uses justIN authentication
    	      and does not require that you have an X.509 proxy or use the
    	      Rucio client. However, it is not as efficient as the standalone
    	      justin-fetch-logs command.
    
           get-token
    	      Download the current WLCG Token cached by justIN for the current
    	      user. This is stored at $BEARER_TOKEN_FILE if set, or
    	      /run/user/UID/bt_uUID if /run/user/UID exists, or /tmp/bt_uUID
    	      in other cases, where UID is the local user's Unix user ID. If
    	      the verbose option is given, the path to the resulting token
    	      file and time left is shown.
    	      While DUNE is still dependent on X.509 proxies for some
    	      storages, this subcommand also requests a DUNE X.509 user proxy
    	      which is authorized to read from Rucio and Rucio-managed
    	      storage. This is stored at $X509_USER_PROXY if set, and at
    	      /tmp/x509up_uUID in other cases.
    	      For both token and proxies files, if the file already exists it
    	      will be overwritten unless the user write permission is unset.
    	      In this case the command will exit with an error. This feature
    	      can be used to protect important proxies or tokens created by
    	      another mechanism from accidental replacement.
    
    
    JOBSCRIPTS
           The user jobscripts supplied when creating a stage are shell scripts
           which the wrapper jobs execute on the worker nodes matched to that
           stage.
    
           When specifying a jobscript to the justin command, either the full,
           local path to the jobscript file is given, or a reference to a tag or
           revison hash in GitHub is given.  (Other git repository services may be
           added in the future.)
    
           A GitHub reference takes the form PATH:TAG where TAG is a git tag or
           SHA1 revision hash, and PATH is the path to the jobscript file in
           GitHub's URL space, of the form
           ORGANISATION/REPO/DIRECTORIES/.../FILE.jobscript .  In both scenarios,
           a copy of the current text of the jobscript is cached in the stage
           definition and executed on worker nodes to process the stage's files.
    
           Jobscripts are run in an empty workspace directory.  Several
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
    
           If no file is available to be processed, then justin-get-file returns a
           non-zero exit code and produces no output to stdout, which should also
           be checked for. justin-get-file logs errors to stderr.
    
           justin-get-file can be called multiple times to process more than one
           file in the same jobscript. This can be done all at the start or
           repeatedly during the lifetime of the job. justin-get-file is itself a
           simple wrapper around the curl command and it would also be possible to
           access the justIN allocator service's REST API directly from an
           application.
    
           justin-get-file has a single option which may also be given:
           --seconds-needed NNNN where NNNN is the maximum number of wallclock
           seconds which will be needed by the jobscript to process another file
           and finish. If there is not enough time left based on the
           --wall-seconds option used when defining the stage, then justin-get-
           file will in that case return an empty result and a non-zero exit code,
           just as if no more files were available for processing. This can easily
           be used to create jobscripts which process a series of input files
           without running out of time on the last one.
    
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
    
    justIN Manual			    justin			  JUSTIN(2024)
