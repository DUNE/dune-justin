# justin-webdav-upload command man page
This man page is distributed along with the 
justin-webdav-upload command itself.

    JUSTIN(2023)							  JUSTIN(2023)
    
    NAME
           justin-webdav-upload - justIN utility to upload files via WebDAV
    
    SYNOPSIS
           justin-webdav-upload [--help] --token-file TOKENFILE --source-file
           SOURCEFILE --destination-directory URL
    
    DESCRIPTION
           justin-webdav-upload is a command-line utility to upload a file using
           WebDAV and a token. It is used by justIN wrapper jobs to upload job
           outputs to scratch disk rather than to Rucio-managed storage. Currently
           it is limited to Fermilab scratch, managed by dCache. You may find it
           useful for some debugging but it is not supported for end-users: you
           should probably use IFDH commands instead.
    
    
    OPTIONS
           -h, --help
    	      Show help message and exit.
    
    
           --token-file TOKENFILE
    	      A SciToken or WLCG profile token in a local file which can be
    	      reached with the absolute or relative path and name TOKENFILE.
    
    
           --source-file SOURCEFILE
    	      A local file to be uploaded which can be reached with the
    	      absolute or relative path and name SOURCEFILE. The filename part
    	      of SOURCEFILE after any final slash is used as the filename on
    	      the remote WebDAV server when uploaded.
    
    
           --destination-directory URL
    	      The URL of a remote WebDAV directory in which to create the
    	      uploaded file.  A trailing slash can be included or omitted.
    	      Parent directories of URL will be created if they do not already
    	      exist. The command will fail with an error if a file with the
    	      name to be created already exists in URL.
    
    
    EXAMPLE
           On a dunegpvm machine at Fermilab, the following creates a token and an
           example file, uploads it to scratch, and then checks it is there via
           pnfs.
    
           htgettoken --debug --vaultserver=htvaultprod.fnal.gov -i dune
           date >/tmp/$USER-date.txt
           justin-webdav-upload \
    	 --token-file  /run/user/`id -u`/bt_u`id -u` \
    	 --source-file /tmp/$USER-date.txt \
    	 --destination-directory \
    	 https://fndcadoor.fnal.gov:2880/dune/scratch/users/$USER/
           ls -l /pnfs/dune/scratch/users/$USER/$USER-date.txt
    
           If you have the token on a remote machine and set --token-file
           accordingly, you should be able to test uploads to Fermilab scratch
           with the command from there.
    
    
    AUTHOR
           Andrew McNab <Andrew.McNab@cern.ch>
    
    
    SEE ALSO
           justin(1)
    
    justIN Manual		     justin-webdav-upload		  JUSTIN(2023)
