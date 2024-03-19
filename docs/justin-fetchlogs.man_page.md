# justin-fetchlogs command man page
This man page is distributed along with the 
justin-fetchlogs command itself.

    JUSTIN(2024)							  JUSTIN(2024)
    
    NAME
           justin-fetchlogs - justIN utility to get logs.tgz file for a given job,
           from Rucio managed storage
    
    SYNOPSIS
           justin-fetchlogs [--help] [--verbose] [--timeout SECONDS] [--unpack]
           JOBSUBID
    
    DESCRIPTION
           justin-fetchlogs is a command-line utility to download and optionally
           unpack the logs.tgz file for a given justIN job.
    
    
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
    	      logs.tgz file. The file is put in the current directiry.
    
    
    AUTHOR
           Andrew McNab <Andrew.McNab@cern.ch>
    
    
    SEE ALSO
           justin(1)
    
    justIN Manual		       justin-fetchlogs 		  JUSTIN(2024)
