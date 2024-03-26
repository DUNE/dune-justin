# justin-fetch-logs command man page
This man page is distributed along with the 
justin-fetchlogs command itself.

    JUSTIN(2024)							  JUSTIN(2024)
    
    NAME
           justin-fetch-logs - justIN utility to get logs.tgz file for a given
           job, from Rucio managed storage
    
    SYNOPSIS
           justin-fetch-logs [--help] [--verbose] [--timeout SECONDS] [--unpack]
           JOBSUBID
    
    DESCRIPTION
           justin-fetch-logs is a command-line utility to download and optionally
           unpack the logs.tgz file for a given justIN job.
    
           This command is more efficient than the justin fetch-logs subcommand
           since the logs.tgz file comes directly from the storage where it was
           uploaded by the job. However, it requires that you have an X.509 proxy
           that Rucio can use to fetch the file.
    
    
    OPTIONS
           -h, --help
    	      Show help message and exit.
    
    
           --verbose
    	      Enables verbose debugging messages.
    
    
           --timeout SECONDS
    	      Timeout in seconds to pass to Rucio.
    
    
           --unpack
    	      Unpack the logs.tgz in the current directory.
    
    
           JOBSUBID
    	      The Jobsub ID of the justIN job for which to retrieve the
    	      logs.tgz file. The file is put in the current directory.
    
    
    AUTHOR
           Andrew McNab <Andrew.McNab@cern.ch>
    
    
    SEE ALSO
           justin(1)
    
    justIN Manual		       justin-fetch-logs		  JUSTIN(2024)
