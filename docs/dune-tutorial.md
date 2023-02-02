## DUNE tutorial

# Prerequisites

This tutorial has been tested on the DUNE interactive VMs at Fermilab and on
lxplus at CERN. It should also work on similar machines elsewhere.

Before following this tutorial, you need to make sure you have the following
in place:

1. Make sure you can create an X.509 proxy, either with kx509 at Fermilab or 
   with grid-proxy-init or voms-proxy-init.
2. Make sure your X.509 DN is in the justIN database, either automatically from
   the DUNE Rucio list of users and X.509 DNs, or added by hand (ask Andrew.)
3. Make sure you can initialise the DUNE UPS environment from cvmfs, by 
   running 
```source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh```

# Checking the prerequisites

Setup DUNE UPS (if you've not already done that within your session),
setup justin from cvmfs and then run the time subcommand.


```
source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh
setup justin
justin time
```

The last command should display the UTC time from the justIN service after
authenticating to the service and after it checks you are authorized.

# Run some hello world jobs

justIN allows requests to consist of multiple stages, but you can create
single stage requests with the quick-request subcommand:

```
justin quick-request --monte-carlo 10 --jobscript-id testpro:hello-world
```

If you execute this command now, justIN will take the jobscript
testpro:hello-world and execute it in 10 jobs which require no input data
files (as if they were Monte Carlo jobs that start from scratch.) Normally 
stages have a list of real input files on storages to process, but for cases
where we want to run a certain number of jobs without inputs from storage,
justIN creates virtual counter files for you, and allocates these to jobs
one by one until they are "used up" when sufficient jobs have run. 

justin quick-request will show you the request ID which is needed to find
logs, jobs status etc. Please take note of that ID now.

You can use 
```justin show-jobscript --jobscript-id testpro:hello-world`` 
to display the script these 10 jobs are running for you. And 
```justin show jobs --request-id REQUEST_ID```
will show you any jobs associated with the request. You need to replace 
REQUEST_ID with the number displayed by quick-request.

The show subcommands are useful for quick checks, but to look at requests
and jobs in detail you need to use the 
[justIn dashboard](https://justin.dune.hep.ac.uk/dashboard/). Go there
and look for the Requests link in navigation the strip at the top of the
page. The request you launched will be listed there, with the REQUEST_ID you
got from the quick-request subcommand.

The page for that request shows interesting things about, and the table
near the bottom of the page has information about its single stage. The
stage is to process 10 files, and they can be in various states from Finding
to Unallocated through to Processed. Clicking on the numbers takes you to
pages with lists of files in each state. 

For each file, you see where it was processed and which Rucio Storage
Element it came from. In the case of our Monte Carlo request, our virtual
MC counter files come from a virtual RSE called MONTECARLO. 

The Jobsub ID at the end of the line is the ID of the HTCondor job in 
which the stage's jobscript was run. Clicking on that ID takes you to a 
very detailed page about that job, including information about the specific
worker node and job slot in which it ran. At the bottom of the page is the
jobscript log which is the merge stdout and stderr of the jobscript that
ran. In this case, it just outputs a Hello world message and the number of
the Monte Carlo virtual file counter.




