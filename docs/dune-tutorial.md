## DUNE tutorial

# Prerequisites

This tutorial has been tested on the DUNE interactive VMs at Fermilab and on
lxplus at CERN. It should also work from similar machines elsewhere.

Before following this tutorial, you need to make sure you have the following
in place:

1. Make sure you can create an X.509 proxy, either with kx509 at Fermilab or
with grid-proxy-init or voms-proxy-init.
2) Make sure your X.509 DN is in the justIN database, either automatically
from the DUNE Rucio list of users and X.509 DNs, or added by hand (ask
Andrew.)
3) Make sure you can initialise the DUNE UPS environment from cvmfs, by
running `source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh`

# Checking the prerequisites

Setup DUNE UPS (if you've not already done that within your session),
setup justin from cvmfs and then run the time subcommand.


```
source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh
setup justin
justin time
```

The last command should display the UTC time from the justIN service, after
authenticating to the service and after it checks you are authorized.

# Run some hello world jobs

justIN allows requests to consist of multiple stages, but you can create
single stage requests with the quick-request subcommand:

```
justin quick-request --monte-carlo 10 --jobscript-id testpro:hello-world
```

If you execute this command now, justIN will take the jobscript
testpro:hello-world and execute it in 10 jobs which require no input data
files (as if they were Monte Carlo jobs that start from scratch.) It will
show you the request ID which is needed to find logs, jobs status etc.

You can use `justin show-jobscript --jobscript-id testpro:hello-world` to
display the script these 10 jobs are running for you. And `justin show jobs
--request-id REQUEST_ID` will show you any jobs associated with the request.
You need to replace REQUEST_ID with the number displayed by quick-request.
