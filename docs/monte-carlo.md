## Monte Carlo requests

justIn relies on matching unprocessed input files with generic
jobs which start on worker nodes at sites. To be able to include Monte Carlo
requests in the system, it is necessary to create virtual counter files in
the [justIn database](database.md)'s list of files. These counter
files are allocated to jobs one by one to keep track of the number of 
Monte Carlo jobs which are required. This framework can be used for other
types of workflow which also do not require real input files from bulk
storage, such as such parameter scanning applications. 

The [justin command man page](justin-man-page.md) explains how to submit
requests in this case. In short, the MQL expression is replaced by
"monte-carlo NNNNNN" where NNNNNN is the number of jobs required. The 
[justin command](justin-command.md) has an option --monte-carlo which
does this.

When the [Finder agent](finder.md) processes a Monte Carlo request, it
creates the correct number of virtual counter files in the database, each
with a name of the form "monte-carlo-RRRRRR-XXXXXX" where RRRRRRR is the 
Request ID number assigned by justIn and XXXXXX is a number
between 000001 and NNNNNN. Each file has a single replica on the virtual RSE
MONTE-CARLO, with PFN consisting just of its XXXXXX number. These file and
replica names are readily accessible within the 
[bootstrap scripts](bootstrap-scripts.md) and so can be
used to derive unique names for the output files, which may be useful for
debugging purposes.


