# DUNE justIN tutorial

[TOC]

## Prerequisites

This tutorial has been tested on the DUNE dunegpvm computers at Fermilab and on
lxplus at CERN. It should also work on similar Linux machines elsewhere but
if you run into problems please use dunegpvmXX or lxplus instead.

You need to be a member of DUNE and have a Fermilab computer account. You
can check this by going to the justIN dashboard at 
[https://dunejustin.fnal.gov/dashboard/](https://dunejustin.fnal.gov/dashboard/)
and logging in: go to that address, click on the orange Login button on the 
top right and follow the instructions. If you get back to the justIN
dashboard with your NAME@fnal.gov shown in place of the Login button, you
have the right registrations.

Before following this tutorial, make sure you can enter an SL7 Apptainer 
container and then initialise the DUNE UPS 
environment from cvmfs and set up justin with these commands:

    /cvmfs/dune.opensciencegrid.org/products/dune/justin/justin-sl7-setup
    source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh
    setup justin
    justin version

You should see a version number displayed. 

## Log in from the command line 

Now we can start the tutorial itself.

Enter an SL7 Apptainer container and set up DUNE UPS and justin if you've not 
already done that within your session:

    /cvmfs/dune.opensciencegrid.org/products/dune/justin/justin-sl7-setup
    source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh
    setup justin

Then run these two commands to clear any existing session and trigger
a new one:

    rm -f /var/tmp/justin.session.`id -u`
    justin time

The justin command will display a message like this:

    To authorize this computer to run the justin command, visit this page with your
    usual web browser and follow the instructions within the next 10 minutes:
    https://dunejustin.fnal.gov/authorize/.........

    Check that the Session ID displayed on that page is ....
 
    Once you've followed the instructions on that web page, please run the command
    you tried again. You won't need to authorize this computer again for 7 days.

Follow those instructions to authorize the justin command to run on your
account on that computer. Then repeat the time subcommand. 

    justin time

It will display the
UTC time from the justIN service and relies on the authorization you've now
set up.

## Run some hello world jobs

justIN allows workflows to consist of multiple stages, but you can create
single stage workflows with the simple-workflow subcommand:

    justin simple-workflow --monte-carlo 10 \
      --jobscript-git DUNE/dune-justin/testing/hello-world.jobscript:01.00.00

If you execute this command now, justIN will take 
hello-world.jobscript from the 
[01.00.00 tag of the justIN repo in GitHub](https://github.com/DUNE/dune-justin/tree/01.00) 
and execute it in 10 jobs which require no input data
files (as if they were Monte Carlo jobs that start from scratch.) 
This mechanism allows you and your group to manage jobscripts in your own 
GitHub repos, with proper versioning, tags, branches etc.

Normally 
stages have a list of real input files on storages to process, but for cases
where we want to run a certain number of jobs without inputs from storage,
justIN creates virtual counter files for you, and allocates these to jobs
one by one until they are "used up" when sufficient jobs have run. 

`justin simple-workflow` will have shown you the workflow ID which is needed to 
find logs, jobs status etc. Please take note of that ID now.

You can use

    justin show-jobscript \
       --jobscript-git DUNE/dune-justin/testing/hello-world.jobscript:01.00.00

to display the script these 10 jobs are running for you. And 

    justin show-jobs --workflow-id WORKFLOW_ID

will show you any jobs associated with the workflow. You need to replace 
WORKFLOW_ID with the number displayed by simple-workflow.

## View your workflow on the justIN web dashboard

The two show subcommands are useful for simple checks, but to look at workflows
and jobs in detail you need to use the 
[justIN dashboard](https://dunejustin.fnal.gov/dashboard/). Go there
and look for the Workflows link in the blue navigation the strip at the top of
the page. The workflow you launched will be listed there, with the WORKFLOW_ID
shown by the simple-workflow subcommand when you ran it.

The page for that workflow shows interesting things about it, and the tables
near the bottom of the page have information about the states of the 
counter files and the jobs which are being run for them. The
stage is to process 10 counter files, and they can be in various states from
Finding to Unallocated through to Processed. Clicking on the numbers takes
you to pages with lists of files or jobs in each state. 

For each file, you see where it was processed and which Rucio Storage
Element it came from. In the case of our Monte Carlo workflow, our virtual
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

To start with, run this command to view the dc4-vd-coldbox-bottom.jobscript
jobscript:

    justin show-jobscript --jobscript-git \
      DUNE/dune-justin/testing/dc4-vd-coldbox-bottom.jobscript:01.00.00

The comments at the top explain how to use the jobscript to process some
VD coldbox files. For this tutorial though, please use these commands:

    MQL_QUERY="files from justin-tutorial:justin-tutorial-2024 limit 10"
    
    justin simple-workflow \
    --mql "$MQL_QUERY" \
    --jobscript-git \
       DUNE/dune-justin/testing/dc4-vd-coldbox-bottom.jobscript:01.00.00 \
    --max-distance 30 \
    --rss-mib 4000 --env NUM_EVENTS=1 --scope usertests \
    --output-pattern '*_reco_data_*.root:output-test' \
    --lifetime-days 1
    
What is this doing?

1. `justin simple-workflow` as before creates a workflow with one stage, in one
go.
2. `--mql "files from ... limit 10"` tells justIN to send the MQL query in
quotes to MetaCat and get a list of matching files. In this case, only the
first 10 matching files are returned. To make it easier to read we've put
the query in `$MQL_QUERY` but you could put it in quotes on the `justin`
command line itself.
3. `--jobscript-git` tells justIN to use the jobscript we've been looking at.
4. `--max-distance 30` says that only replicas of files within a distance of
30 from where the job is running will be considered. In practice, 30 means 
within North America or within Europe, but not from one to the other. 
5. `--rss-mib 4000` asks for 4000 MiB of memory. Since `--processors` is not
given, the default of 1 processor is workflowed.
6. `--env NUM_EVENTS=1` sets the environment variable NUM_EVENTS. If you
look back at the jobscript you will see this variable causes LArSoft to
process just 1 event from the input file it is given.  
7. `--scope usertests` says that output files will be created with the Rucio
scope usertests, which any DUNE member can write to. Output files will be
created with Rucio Data Identifiers (DIDs) like usertests:aaaa.root
8. `--output pattern '*_reco_data_*.root:output-test'` tells justIN to
look for output files matching the shell wildcard expression
`*_reco_data_*.root` in the working directory of the jobscript, when it
finishes. `output-test` is the prefix to a name of a Rucio dataset to 
add the output
files to, and the full name of that dataset is `usertests:output-test` 
plus `-wXXXXs1p1` where XXXX is the ID number of the workflow created. Make
sure each file put into storage has a unique filename, otherwise the
outputting step will fail. 
9. `--lifetime-days` says that the output files are only guaranteed to persist
on storage for 1 day.

The command doesn't tell justIN where to put the output files. There are
options to try to steer outputs to particular groups of storages, but with
the example command above they will be written to the closest accessible
storage, based on where the job is running. The outputs are all registered
in Rucio, so it's still easy to find them wherever they are written. 

Go ahead and do the `justin simple-workflow` command shown above, and then
watch its progress via the justIN dashboard. Find the workflow's page and 
look at the states of the input files and the jobs being created in the 
tables on that page.

Once all the files get to terminal states (processed, failed etc) then
justIN sets the state of the workflow itself to finished and stops allocating
any more jobs to it.

## Fetching files from Rucio managed storage

Leave the Apptainer container if you are already in one. To use Rucio 
do these setup steps:

    /cvmfs/dune.opensciencegrid.org/products/dune/justin/justin-sl7-setup
    source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh
    setup python v3_9_15
    setup rucio
    setup justin

This changes the Python version to one needed by `rucio`, and tells `justin`
to use the same one.

You should be able to continue using the same justIN session you've already
setup but the `justin` command will ask you to authorize a new sesssion if
necessary. But to use the `rucio` command and storage, you also need an X.509
VOMS Proxy. You can get one from justIN that gives read-only access with this 
command:

    justin get-token

The proxy will normally be created in `/tmp/x509up_uXXXXX` where XXXXX is your
Unix user ID, given by `id -u` .
This also gets you a DUNE WLCG Token and eventually the X.509 feature will 
be dropped from it. You need to tell `rucio` to use the DUNE read-only account
and then you can start running `rucio` commands:

    export RUCIO_ACCOUNT=justinreadonly
    rucio whoami
    rucio list-scopes

When your jobs finish, the list of files they have each outputted is shown on 
the pages for the individual jobs which we talked about earlier. You can
download one or two from Rucio managed storage with the `rucio get`
subcommand.

Since I don't know what your output files will be called, let's use one of
the input files as an example, and run the command in a personal temporary
directory:

    mkdir -p /tmp/$USER
    cd /tmp/$USER
    rucio get justin-tutorial:tut_np02bde_307160127\
    _np02_bde_coldbox_run012352_0057_20211216T001236.hdf5

This file is about 4GB in size so it takes a few seconds to fetch. Some of
the Rucio error messages look alarming but let the command finish. The
`rucio` command finds the list of replicas of that file and picks one 
replica to download. It puts it in subdirectory named after the scope
`justin-tutorial`.

## Jobs using GPUs ##

It's very easy to access NVIDIA GPUs on the grid using justIN: just add the
`--gpu` option to the `justin simple-workflow` command and the jobs for your
workflow will be directed to machines with GPUs and one GPU will be
requested for each job.

In more detail, the full command to submit a "Hello GPU" workflow looks like
this:

    justin simple-workflow --monte-carlo 10 --gpu \
      --jobscript-git DUNE/dune-justin/testing/hello-gpu.jobscript:01.04.rc0

You could add more options to save output files as we did already, but for now
just submit the workflow and look at the jobscript logs on the justIN 
dashboard.
Due to the finite number of GPUs available on the grid, you might find that
sometimes a workflow starts within minutes, but if you're really unlucky it
might take hours to find enough free slots.

The jobscript you've used is very similar to the Hello World one we started
with, but has two extra GPU lines:

    printenv | grep -i cuda
    nvidia-smi

These print out all the environment variables with variants of CUDA in the
name. The important one is based on what the GlideInWMS pilot job tells
justIN and looks something like this:

    CUDA_VISIBLE_DEVICES=GPU-3ae786cc-80fb-24fd-16ad-8191bd0341d2

That environment varible is used by CUDA applications to decide which GPUs to
use if more than one is available. Please don't try to override that in your
jobscript.

The next command is the `nvidia-smi` utility which tells you more about the
GPUs that are available on the machine, including the one you can use. It
shows details of the model, memory usage, and even things like temperature.

If you have a GPU enabled application that uses CUDA, it should be
straightforward to get it running in a justIN workflow. Apptainer and the
GlideInWMS pilot make sure the NVIDIA libraries installed on the worker
node, including the non-free software, is available to your jobs through
`$LD_LIBRARY_PATH` and the special directory `/.singularity.d/libs/` 

## Jobs writing to scratch ##

Instead of uploading outputs to Rucio-managed storage, it's also possible to
make jobs upload outputs to scratch space. Currently this only works to
/pnfs/dune/scratch/users/USERNAME at Fermilab but we plan to add uploads to
EOS scratch space at CERN in the future.

To follow this section of the tutorial you do not strictly need to be logged
in to a dunegpvm machine at Fermilab, as you can access files on scratch 
remotely using GFAL tools. However, it is easier to check from a dunegpvm
machine as you can look in /pnfs/dune/scratch/users/$USER where $USER is your
Fermilab username using Unix commands. 

We can adapt the DC4 example from the previous section to use scratch for
outputs like this. If you are not on a dunegpvm, replace `$USER` with your
Fermilab username.

    USERF=$USER
    FNALURL='https://fndcadoor.fnal.gov:2880/dune/scratch/users'
    MQL_QUERY="files from justin-tutorial:justin-tutorial-2024 limit 10" 
    
    justin simple-workflow \
    --mql "$MQL_QUERY" \
    --jobscript-git \
       DUNE/dune-justin/testing/dc4-vd-coldbox-bottom.jobscript:01.00.00 \
    --max-distance 30 \
    --rss-mib 4000 --env NUM_EVENTS=1 \
    --output-pattern "*_reco_data_*.root:$FNALURL/$USERF"

If you are on a dunegpvm machine, you can view the output directory
by just using ls, after replacing 00000 with the ID number of your workflow
including leading zeros:

    ls /pnfs/dune/scratch/users/$USER/000000/1/

From anywhere you have GFAL commands and an X.509 proxy, this should work,
again after replacing 00000 with the ID number of your workflow
including leading zeros:

    gfal-ls https://fndcadoor.fnal.gov:2880/dune/scratch/users/$USERF/00000/1

The usual caveats about Fermilab dCache scratch apply: it's not backed up,
and files will eventually be deleted automatically as other users create new
files and fill the space up. So you want to copy anything important to 
persistent storage of some form. You should also not flood the scratch
space unnecessarily, as it will prematurely evict other people's temporary
files.

## Interactive testing of jobscripts 

If you need to create or modify jobscripts yourself then you need to learn
how to test them. This is especially important since you do not want to
create thousands of failing jobs, wasting your time, wasting the site's
hardware, and wasting electricity.

justIN provides the command `justin-test-jobscript` which allows you to run a
jobscript interactively on your computer. In jobs at remote sites, justIN runs
your jobscripts inside an Apptainer container. The `justin-test-jobscript`
command runs your jobscript using the same container format and so provides
a very realistic test of your script. The command is available to you after 
using the same `setup justin` command as for `justin` itself. It's not
necessary to have Apptainer or Singularity installed as the command gets
Apptainer from cvmfs.

`justin-test-jobscript` will obtain a DUNE VOMS proxy for your script,
just as justIN does for jobscripts running as jobs. The proxy file path
is given by the environment variable `$X509_USER_PROXY`. Commands like
`xrdcp` and `lar` use this variable to find the proxy automatically. You
should not try to write to storage from your jobscript though. In jobs,
justIN handles that for you using the `--output-pattern` mechanism and the
proxy your jobscript will have there does not have write privileges itself.

Let's rerun the Data Challenge 4 jobscript we used in the previous section,
but this time use a local file and run it interactively. First get a copy
of the jobscript in your current directory:

    justin show-jobscript --jobscript-git \
      DUNE/dune-justin/testing/dc4-vd-coldbox-bottom.jobscript:01.00.00 \
      > my-dc4-vd-coldbox-bottom.jobscript

Have a look at it with your favourite text editor and maybe add an extra
line  before the fcl file comment. So it reads:

    echo 'My version of this jobscript!'
    # fcl file and DUNE software version/qualifier to be used

Now run it with `justin-test-jobscript`. All of the files it creates are
made under /tmp in the directory name it prints out.

    MQL_QUERY="files from justin-tutorial:justin-tutorial-2024 limit 10" 
    
    justin-test-jobscript --mql "$MQL_QUERY" \
     --jobscript my-dc4-vd-coldbox-bottom.jobscript \
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
simple-workflow with these options:

    MQL_QUERY="files from justin-tutorial:justin-tutorial-2024 limit 10" 
    
    justin simple-workflow \
    --mql "$MQL_QUERY" \
    --jobscript my-dc4-vd-coldbox-bottom.jobscript --max-distance 30 \
    --rss-mib 4000 --env NUM_EVENTS=1 --scope usertests \
    --output-pattern '*_reco_data_*.root:output-test' \
    --lifetime-days 1

As you can see, you just need to change the whole
`--jobscript-git` option to 
`--jobscript my-dc4-vd-coldbox-bottom.jobscript` 
to use the local file as the jobscript.
    
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
You don't need to be on a Fermilab computer for this step but you **must**
make a tar file, not one file by itself or a tar.gz file.

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

    justin get-token
    INPUT_TAR_DIR_LOCAL=`justin-cvmfs-upload hello_world.tar`
    echo $INPUT_TAR_DIR_LOCAL

The first line makes sure you have a Bearer Token in place (probably at
/run/users/UID/bt_uUID where UID is your Unix user ID.) You don't need to
know your UID to use the command but it might help with debugging.

The second line runs `justin-cvmfs-upload` to send your tar file to the RCDS
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

It may take a bit longer for the cvmfs files to propogate to remote sites,
and you should bear that in mind if you see errors in the jobs. 
These files are likely to last about a month in cvmfs before they
expire, but you should rerun the commands shown above to upload the tar file
each day you submit workflows that rely on it. Keep the same tar file and 
reupload that, as RCDS records a hash of it and does not unpack a tar file
it already has. 

Since you know the directory contained in `$INPUT_TAR_DIR_LOCAL`, you could
just hard code it in your jobscripts. But it's simpler to pass the
environment variable itself to jobscripts. 

Look at this example jobscript:
 
    justin show-jobscript --jobscript-git \
      DUNE/dune-justin/testing/cvmfs-hello-world.jobscript:01.00.00

The important lines are right at the end:

    # Look at the file in cvmfs
    echo "Contents of $INPUT_TAR_DIR_LOCAL/hello_world.txt"
    cat $INPUT_TAR_DIR_LOCAL/hello_world.txt

You can see it will use a local copy of the environment variable 
`$INPUT_TAR_DIR_LOCAL` to find the
`hello_world.txt` file in cvmfs and print it out. 

This command creates a workflow to run it:

    justin simple-workflow --monte-carlo 1 \
     --env INPUT_TAR_DIR_LOCAL="$INPUT_TAR_DIR_LOCAL" \
     --jobscript-git \
        DUNE/dune-justin/testing/cvmfs-hello-world.jobscript:01.00.00

The `--env` line takes the `$INPUT_TAR_DIR_LOCAL` value from your computer
and then tells justIN to set an environment variable with the same name
when it runs the jobscript. 

Try this now and look at the output through the dashboard.

## More information

There is a lot more about justIN in the docs area at
[https://dunejustin.fnal.gov/docs/](https://dunejustin.fnal.gov/docs/)

When you `setup justin`, you also get the justin, justin-test-jobscript,
and justin-cvmfs-upload  man pages.
