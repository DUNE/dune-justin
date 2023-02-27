# DUNE justIN tutorial

**THIS TUTORIAL IS STILL IN A DRAFT STATE AND NOT READY FOR NEW USERS**

## Prerequisites

This tutorial has been tested on the DUNE dunegpvm computers at Fermilab and on
lxplus at CERN. It should also work on similar Linux machines elsewhere but
if you run into problems please use dunegpvmXX or lxplus instead.

You need to be a member of DUNE and have a Fermilab computer account. You
can check this by going to the justIN dashboard at 
[https://justin.dune.hep.ac.uk/dashboard/](https://justin.dune.hep.ac.uk/dashboard/)
and logging in: go to that address, click on the orange Login button on the 
top right and follow the instructions. If you get back to the justIN
dashboard with your NAME@fnal.gov shown in place of the Login button, you
have the right registrations.

For one section of the tutorial you will need to be able to create a VOMS
proxy with the command `voms-proxy-init`, which anyone in DUNE should be
able to do.

Before following this tutorial, make sure you can initialise the DUNE UPS 
environment from cvmfs and set up justin with these commands:

    source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh
    setup justin
    justin version

You should see a version number displayed. 

## Log in from the command line 

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
testpro:hello-world from justIN's Jobscripts Library
and execute it in 10 jobs which require no input data
files (as if they were Monte Carlo jobs that start from scratch.) Normally 
stages have a list of real input files on storages to process, but for cases
where we want to run a certain number of jobs without inputs from storage,
justIN creates virtual counter files for you, and allocates these to jobs
one by one until they are "used up" when sufficient jobs have run. 

`justin quick-request` will have shown you the request ID which is needed to 
find logs, jobs status etc. Please take note of that ID now.

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

The page for that request shows interesting things about it, and the tables
near the bottom of the page have information about the states of the 
counter files and the jobs which are being run for them. The
stage is to process 10 counter files, and they can be in various states from
Finding to Unallocated through to Processed. Clicking on the numbers takes
you to pages with lists of files or jobs in each state. 

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

The real power of justIN is in matching files and jobs based on locations.
To see this in action we need to learn how to specify the input files to
process and understand how outputs are specified and where they are put.

This section uses a workflow from Data Challenge 4 and shows you
how to repeat part of it. We'll run LArSoft to process some data that is
registered in MetaCat and Rucio, and temporarily store the output files in
Rucio-managed storage at remote sites.

To start with, run this command to view the dc4-vd-coldbox-top:default
jobscript:

    justin show-jobscript --jobscript-id dc4-vd-coldbox-top:default

The comments at the top explain how to use the jobscript to process some
VD coldbox files. For this tutorial though, please use this command:

    justin quick-request \
    --mql \
    "files from dc4:dc4 where core.run_type='dc4-vd-coldbox-top' limit 10" \
    --jobscript-id dc4-vd-coldbox-top:default --max-distance 30 \
    --rss-mb 4000 --env NUM_EVENTS=1 --scope usertests \
    --output-pattern '*_reco_data_*.root:output-test-01'
    
What is this doing?

1. `justin quick-request` as before creates a request with one stage, in one
go.
2. `--mql "files from ... limit 10"` tells justIN to send the MQL query in
quotes to MetaCat and get a list of matching files. In this case, only the
first 10 matching files are returned.
3. `--jobscript-id` tells justIN to use the jobscript we've been looking at.
4. `--max-distance 30` says that only replicas of files within a distance of
30 from where the job is running will be considered. In practice, 30 means 
within North America or within Europe, but not from one to the other. 
5. `--rss-mb 4000` asks for 4000 MiB of memory. Since `--processors` is not
given, the default of 1 processor is requested.
6. `--env NUM_EVENTS=1` sets the environment variable NUM_EVENTS. If you
look back at the jobscript you will see this variable causes LArSoft to
process just 1 event from the input file it is given.  
7. `--scope usertests` says that output files will be created with the Rucio
scope usertests, which any DUNE member can write to. Output files will be
created with Rucio Data Identifiers (DIDs) like usertests:aaaa.root
8. `--output pattern '*_reco_data_*.root:output-test-01'` tells justIN to
look for output files matching the shell wildcard expression
`*_reco_data_*.root` in the working directory of the jobscript, when it
finishes. `output-test-01` is the name of a Rucio dataset to add the output
files to, and the full name of that dataset is `usertests:output-test-01`.

The command doesn't tell justIN where to put the output files. There are
options to try to steer outputs to particular groups of storages, but with
the example command above they will be written to the closest accessible
storage, based on where the job is running. The outputs are all registered
in Rucio, so it's still easy to find them wherever they are written. 

Go ahead and do the `justin quick-request` command shown above, and then
watch its progress via the justIN dashboard. Find the request's page and 
look at the states of the input files and the jobs being created in the 
tables on that page.

Once all the files get to terminal states (processed, failed etc) then
justIN sets the state of the request itself to finished and stops allocating
any more jobs to it.

## Interactive testing of jobscripts 

If you need to create or modify jobscripts yourself then you need to learn
how to test them. This is especially important since you do not want to
create thousands of failing jobs, wasting your time, wasting the site's
hardware, and wasting electricity.

justIN provides the script `justin-test-jobscript` which allows you to run a
jobscript interactively on your computer. In jobs at remote sites, justIN runs
your jobscripts inside a Singularity container. The `justin-test-jobscript`
command runs your jobscript using the same container format and so provides
a very realistic test of your script. The command is available to you after 
using the same `setup justin` command as for `justin` itself.

If your jobscript reads from remote storage, you also need to have a valid
DUNE VOMS proxy created with voms-proxy-init. On a dunegpvm computer
do something like this:

    rm -f /tmp/x509up_u`id -u`
    kx509
    voms-proxy-init -noregen -rfc -voms dune:/dune/Role=Analysis

If you normally do something else to run `voms-proxy-init` and get a VOMS
proxy with the Analysis role, then do that.

`justin-test-jobscript` will pass this proxy to
your jobscript using the environment variable `$X509_USER_PROXY`. Commands like
`xrdcp` and `lar` use this variable to find the proxy automatically. You
should not try to write to storage from your jobscript though. In jobs,
justIN handles that for you using the `--output-pattern` mechanism and the
proxy your jobscript will have there does not have write privileges itself.

Let's rerun the Data Challenge 4 jobscript we used in the previous section,
but this time use a local file and run it interactively. First get a copy
of the jobscript in your current directory:

    justin show-jobscript --jobscript-id dc4-vd-coldbox-top:default \
      > my-dc4-vd-coldbox-top.jobscript

Have a look at it with your favourite text editor and maybe add an extra
line  before the fcl file comment. So it reads:

    echo 'My version of this jobscript!'
    # fcl file and DUNE software version/qualifier to be used

Now run it with `justin-test-jobscript`. All of the files it creates are
made under /tmp in the directory name it prints out.

    justin-test-jobscript --mql \
     "files from dc4:dc4 where core.run_type='dc4-vd-coldbox-top' limit 10" \
     --jobscript my-dc4-vd-coldbox-top.jobscript \
     --env NUM_EVENTS=1

This should only take a couple of minutes to run as we limited it to process
one event. Even though the MQL still says `limit 10`, only one input file
is given to the jobscript. You will see the output of the commands inside the 
jobscript as they happen, and the output ends with a directory listing of the 
workspace directory where they all ran. 
This is left in place so you can look through the outputs and any logs 
you created. If you produced any large files, please 
delete the directory in /tmp when you're finished.

If you want to test your jobscript running in real jobs, you can repeat the
quick-request with these options:

    justin quick-request \
    --mql \
    "files from dc4:dc4 where core.run_type='dc4-vd-coldbox-top' limit 10" \
    --jobscript my-dc4-vd-coldbox-top.jobscript --max-distance 30 \
    --rss-mb 4000 --env NUM_EVENTS=1 --scope usertests \
    --output-pattern '*_reco_data_*.root:output-test-01'

As you can see, you just need to change 
`--jobscript-id dc4-vd-coldbox-top:default` to the option  
`--jobscript my-dc4-vd-coldbox-top.jobscript` to use the local file as the
jobscript.
    
## Rapid Code Distribution to jobs via cvmfs

Part of this section has to be done on a computer inside the Fermilab 
firewall. Once this is done, you can do the rest on lxplus or other
computers where you have set up the `justin` command.

One of the best features of Jobsub is that it can create temporary
directories in cvmfs with collections of files your jobs need. This uses
Fermilab's Rapid Code Distribution Service (RCDS) and makes your files 
available to your jobs at all conventional OSG and WLCG sites.

This section shows you how to do this for justIN jobs too, using the 
`justin-cvmfs-upload` command, which is available to you after 
using the same `setup justin` command as for `justin` itself.

First, you need to make a tar file containing the files you want to include.
You don't need to be on a Fermilab computer for this step.

    mkdir somedir
    cd somedir
    date > hello_world.txt
    tar cvf hello_world.tar *

Notice that you're not tarring up a
directory. You are adding the individual files to make the tar file
`hello_world.tar`. In this case the * wildcard character gets everything but
you could list them individually if you want.

Next, **on a Fermilab dunegpvm computer** which has the justin commands set 
up like this if not already done so:

    source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh
    setup justin

and a copy of `hello_world.tar` in the current directory, do this:

    rm -f /tmp/x509up_u`id -u`
    kx509
    INPUT_TAR_DIR_LOCAL=`justin-cvmfs-upload hello_world.tar`
    echo $INPUT_TAR_DIR_LOCAL

The first two lines make sure you have a valid X.509 proxy in place. If you
need a VOMS proxy later on you'll need to rerun that too, but it's not
needed for the rest of the tutorial.

The third line runs `justin-cvmfs-upload` to send your tar file to the RCDS
server. It waits until RCDS has unpacked the tar file and then puts the cvmfs
directory in which it was unpacked in the environment variable 
`$INPUT_TAR_DIR_LOCAL` You can use any name you like for that but I've
picked that name to match the name used by Jobsub. If necessary, you can
also upload more than one tar file and use them in the same jobscript, but 
then you need to keep track of
their directory names with different environment variables.

Waiting for RDCS to return should only have taken about a minute, but it
will take a few more minutes for the files to be visible on cvmfs. 

The rest of this section does not have to be done at Fermilab, and so you 
can switch back to lxplus if you were using it before. You need
to make sure INPUT_TAR_DIR_LOCAL is set if you do change computers though.

You can check the file's state in cvmfs using the environment variable. At 
first you'll get `No such file or directory errors` but once it's there, 
you can see the file in place with:

    ls -l $INPUT_TAR_DIR_LOCAL

It may take a bit longer for the cvmfs files to propogate to remove sites,
and you should bear that in mind if you see errors in the jobs. 
These files are likely to last about a month in cvmfs before they
expire, but you should rerun the commands shown above to upload the tar file
each day you submit requests that rely on it. Keep the same tar file and 
reupload that, as RCDS records a hash of it and does not unpack a tar file
it already has. 

Since you know the directory contained in `$INPUT_TAR_DIR_LOCAL`, you could
just hard code it in your jobscripts. But it's simpler to pass the
environment variable itself to jobscripts. 

Look at this example jobscript:

    justin show-jobscript --jobscript-id testpro:cvmfs-hello-world

The important lines are right at the end:

    # Look at the file in cvmfs
    echo "Contents of $INPUT_TAR_DIR_LOCAL/hello_world.txt"
    cat $INPUT_TAR_DIR_LOCAL/hello_world.txt

You can see it will use a local copy of the environment variable 
`$INPUT_TAR_DIR_LOCAL` to find the
`hello_world.txt` file in cvmfs and print it out. 

This command creates a request to run it:

    justin quick-request --monte-carlo 1 \
     --env INPUT_TAR_DIR_LOCAL="$INPUT_TAR_DIR_LOCAL" \
     --jobscript-id testpro:cvmfs-hello-world

The `--env` line takes the `$INPUT_TAR_DIR_LOCAL` value from your computer
and then tells justIN to set an environment variable with the same name
when it runs the jobscript. 

Try this now and look at the output through the dashboard.

## More information

There is a lot more about justIN in the docs area at
[https://justin.dune.hep.ac.uk/docs/](https://justin.dune.hep.ac.uk/docs/)

When you `setup justin`, you also get the justin man page and 
[that's on the website](https://justin.dune.hep.ac.uk/docs/justin_command.man_page.md)
too.
