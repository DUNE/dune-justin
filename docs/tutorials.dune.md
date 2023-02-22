# DUNE justIN tutorial

**THIS TUTORIAL IS STILL IN A DRAFT STATE AND NOT READY FOR NEW USERS**

## Prerequisites

This tutorial has been tested on the DUNE dunegpvm machines at Fermilab and on
lxplus at CERN. It should also work on similar Linux machines elsewhere but
if you run into problems please use dunegpvmXX or lxplus instead.

You need to be a member of DUNE and have a Fermilab computer account. You
can check this by going to the justIN dashboard at 
[https://justin.dune.hep.ac.uk/dashboard/](https://justin.dune.hep.ac.uk/dashboard/)
and logging in: go to that address, click on the orange Login button on the 
top right and follow the instructions. If you get back to the justIN
dashboard with your NAME@fnal.gov shown in place of the Login button, you
have the right registrations.

Before following this tutorial, make sure you can initialise the DUNE UPS 
environment from cvmfs and set up justin with these commands:

    source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh
    setup justin
    justin version

You should see a version number displayed. 

## Logging in from the command line 

Now we can start the tutorial itself.

Set up DUNE UPS and justin if you've not already done that within your
session:

    source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh
    setup justin

Then run these two commands to clear any existing session and trigger
a new one:

    rm -f /var/tmp/justin.session.`id -u`
    justin time

The justin command will display a message like this:

    To authorize this computer to run the justin command, visit this page with your
    usual web browser and follow the instructions within the next 10 minutes:
    https://justin.dune.hep.ac.uk/authorize/.........

    Check that the Session ID displayed on that page is .......

    Once you've followed the instructions on that web page, you can run the justin
    command without needing to authorize this computer again for 7 days.

Follow those instructions to authorize the justin command to run on your
account on that computer. Then repeat the time subcommand. 

    justin time

It will display the
UTC time from the justIN service and relies on the authorization you've now
set up.

## Run some hello world jobs

justIN allows requests to consist of multiple stages, but you can create
single stage requests with the quick-request subcommand:

    justin quick-request --monte-carlo 10 --jobscript-id testpro:hello-world

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

    justin show-jobscript --jobscript-id testpro:hello-world

to display the script these 10 jobs are running for you. And 

    justin show-jobs --request-id REQUEST_ID

will show you any jobs associated with the request. You need to replace 
REQUEST_ID with the number displayed by quick-request.

## View your request on the justIN web dashboard

The two show subcommands are useful for quick checks, but to look at requests
and jobs in detail you need to use the 
[justIN dashboard](https://justin.dune.hep.ac.uk/dashboard/). Go there
and look for the Requests link in the blue navigation the strip at the top of
the page. The request you launched will be listed there, with the REQUEST_ID
shown by the quick-request subcommand when you ran it.

The page for that request shows interesting things about it, and the table
near the bottom of the page has information about its single stage. The
stage is to process 10 counter files, and they can be in various states from
Finding to Unallocated through to Processed. Clicking on the numbers takes
you to pages with lists of files in each state. 

For each file, you see where it was processed and which Rucio Storage
Element it came from. In the case of our Monte Carlo request, our virtual
MC counter files come from a virtual RSE called MONTECARLO. 

The Jobsub ID at the end of the line is the ID of the HTCondor job in 
which the stage's jobscript was run. Clicking on that ID takes you to a 
very detailed page about that job, including information about the specific
worker node and job slot in which it ran. At the bottom of the page is the
jobscript log which is the merged stdout and stderr of the jobscript that
ran. In this case, the jobscript just outputs a Hello world message and the 
number of the Monte Carlo virtual file counter.

## Jobs with inputs and outputs

## Interactive testing of jobscripts 

## Rapid Code Distribution to jobs via cvmfs

Part of this section has to be done on a computer at Fermilab. 
