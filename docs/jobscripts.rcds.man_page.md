# justin-cvmfs-upload command man page
This man page is distributed along with the 
justin-cvmfs-upload command itself.

    JUSTIN(2023)                                                      JUSTIN(2023)
    
    
    
    NAME
           justin-cvmfs-upload - upload files to cvmfs via RCDS for justIN
    
    SYNOPSIS
           justin-cvmfs-upload [--help] [--verbose] TAR_FILE
    
    DESCRIPTION
           justin-cvmfs-upload  is  a  command-line utility for upload one or more
           files contained in a tar archive file to cvmfs using the Fermilab Rapid
           Code Distribution Service (RCDS). The full cvmfs path is then output by
           the command.
    
    
    OPTIONS AND ARGUMENTS
           -h, --help
                  Show help message and exit.
    
    
           -v, --verbose
                  Turn on verbose logging.
    
    
           TAR_FILE
                  A .tar archive file (not a tar.tgz compressed archive!) contain-
                  ing files to be uploaded to cvmfs via RCDS.
    
    
    EXAMPLE
           justin-cvmfs-upload must be run on a computer inside the Fermilab fire-
           wall. You also need a valid X.509 proxy, which you can  readily  create
           with the kx509 commnad. A VOMS proxy is not needed.
    
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
    
    
    
    justIN Manual                 justin-cvmfs-upload                 JUSTIN(2023)
