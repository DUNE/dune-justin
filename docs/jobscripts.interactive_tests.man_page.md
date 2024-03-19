# justin-test-jobscript command man page
This man page is distributed along with the 
justin-test-jobscripts command itself.

    JUSTIN(2024)							  JUSTIN(2024)
    
    NAME
           justin-test-jobscript - interactive testing of justIN jobscripts
    
    SYNOPSIS
           justin-test-jobscript [--help] --jobscript FILENAME --mql
           MQL|--monte-carlo COUNT [--env NAME=VALUE]
    
    DESCRIPTION
           justin-test-jobscript is a command-line utility to test jobscripts
           which normally run inside justIN jobs on the grid. The jobscripts are
           run with Apptainer using the same container format as for jobs,
           providing a very realistic test. The options to the command have the
           same functions as the corresponding options to the justin command.
    
           If the jobscript reads from remote storage, you need to have a valid
           DUNE VOMS proxy when the justin-test-jobscript command is run, either
           at /tmp/x509up_u`id -u` or in the location indicated by
           $X509_USER_PROXY. A copy of the proxy is made and made available to the
           jobscript inside the container via $X509_USER_PROXY.
    
           The command displays the output of the jobscript while it is running
           and then lists the files produced, which are left in the container's
           working directory which you can examine.
    
    
    OPTIONS AND ARGUMENTS
           -h, --help
    	      Show help message and exit.
    
    
           --jobscript FILENAME
    	      Filename of the jobscript to be tested.
    
    
           --mql MQL
    	      MetaCat MQL expression use to find input files.
    	      justin-test-jobscript uses the justin show-replicas command to
    	      find the replicas using MetaCat and Rucio queries by the justIN
    	      service.	This option is required if --monte-carlo is not given.
    
    
           --monte-carlo COUNT
    	      This causes a Monte Carlo counter file to be given to the
    	      jobscript instead of an input file found from MetaCat.  This
    	      option is required if --mql is not given.
    
    
           --env NAME=VALUE
    	      This option can be used one or more times to define environment
    	      variables which will be set inside the container.
    
    
    EXAMPLE
           In this example we make a local copy of a jobscript from the Jobscripts
           Library and then run it using the justin-test-jobscript command, using
           the jobscript's $NUM_EVENTS variable to limit processing to the first
           event of the input file.
    
           justin show-jobscript --jobscript-id dc4-vd-coldbox-top:default \
    	 > my-dc4-vd-coldbox-top.jobscript
    
           justin-test-jobscript --mql \
    	"files from dc4:dc4 where core.run_type='dc4-vd-coldbox-top' limit 10" \
    	--jobscript my-dc4-vd-coldbox-top.jobscript \
    	--env NUM_EVENTS=1
    
    
    
    AUTHOR
           Andrew McNab <Andrew.McNab@cern.ch>
    
    
    SEE ALSO
           justin(1)
    
    justIN Manual		     justin-test-jobscript		  JUSTIN(2024)
