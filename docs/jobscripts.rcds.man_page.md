# justin-cvmfs-upload command man page
This man page is distributed along with the 
justin-cvmfs-upload command itself.

    JUSTIN(2024)							  JUSTIN(2024)
    
    NAME
           justin-cvmfs-upload - upload files to cvmfs via RCDS for justIN
    
    SYNOPSIS
           justin-cvmfs-upload [--help] [--verbose] TAR_FILE
    
    DESCRIPTION
           justin-cvmfs-upload is a command-line utility for uploading one or more
           files contained in a tar archive file to cvmfs using the Fermilab Rapid
           Code Distribution Service (RCDS). The full cvmfs path is then output by
           the command.
    
           The environment variable JOBSUB_DROPBOX_SERVER_LIST is used to find a
           random RCDS server to use, or rcds01.fnal.gov if the variable is not
           set.
    
    
    OPTIONS AND ARGUMENTS
           -h, --help
    	      Show help message and exit.
    
    
           -v, --verbose
    	      Turn on verbose logging.
    
    
           TAR_FILE
    	      A .tar archive file (not a tar.tgz compressed archive!)
    	      containing files to be uploaded to cvmfs via RCDS.
    
    
    EXAMPLE
           justin-cvmfs-upload must be run on a computer inside the Fermilab
           firewall. You also need a valid Bearer Token for your UID at
           /run/users/UID/bt_uUID which you can readily create with the command
           htgettoken
    
           htgettoken -a htvaultprod.fnal.gov -i dune
           mkdir somedir
           cd somedir
           date > hello_world.txt
           tar cvf hello_world.tar *
           INPUT_TAR_DIR_LOCAL=`justin-cvmfs-upload hello_world.tar`
           echo $INPUT_TAR_DIR_LOCAL
    
    
    AUTHOR
           Andrew McNab <Andrew.McNab@cern.ch>
    
    
    SEE ALSO
           justin(1)
    
    justIN Manual		      justin-cvmfs-upload		  JUSTIN(2024)
