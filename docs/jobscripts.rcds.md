# Rapid Code Distribution Service

One of the best features of Jobsub is that it can create temporary
directories in cvmfs with collections of files your jobs need. This uses
Fermilab's Rapid Code Distribution Service (RCDS) and makes your files 
available to your jobs at all conventional OSG and WLCG sites.

You can do the same for justIN jobs using the 
`justin-cvmfs-upload` command, which is available to you after 
using the same `setup justin` command as for `justin` itself.

See the RCDS section of the [DUNE Tutorial](tutorials.dune.md)
and the [justin-cvmfs-upload](jobscripts.rcds.man_page.md) 
man page.

