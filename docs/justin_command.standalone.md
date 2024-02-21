## Standalone justin command setup

The supported way to set up the [justin command](justin_command.md)
is to set up the DUNE environment and then do `setup justin` just as with 
other DUNE packages, either on a
dunegpvm machine at Fermilab or on CERN's lxplus. If you run into problems,
please replicate them on those platforms before reporting them.

If you are using a Linux machine elsewhere that has cvmfs, it may still be 
possible to set up the DUNE environment and use `setup justin` there too.

If you are on a Linux or macOS machine without cvmfs, then this page
explains how to do a standalone install of the `justin` command.

The command is a self-contained Python3 script, which has no dependencies 
beyond the standard modules provided with Python 3.6 and above. There is no
need to install additional modules, Rucio, token handling, or X.509 CA
certificates.

The first step is to get the `justin` script.

If you have access to a machine with cvmfs, then the current production
version can always be copied from 

    /cvmfs/dune.opensciencegrid.org/products/dune/justin/pro/NULL/bin/justin

Otherwise, you can get it from the
[commands directory in the justIN repo on GitHub](https://github.com/DUNE/dune-justin/tree/main/commands). 
Check what version is displayed at the bottom of any page on the production
justIN dashboard (including this one). Then select the major.minor branch
on GitHub. For example, if the current version is 00.13.06, select the head
of the branch 00.13 

Once you have a copy of the `justin` script on your own machine, copy it
to somewhere on your unix $PATH and make sure it is executable. 
Somewhere like $HOME/bin is a good choice but you might need to set that up 
on your machine first (all this depends on your OS).

Then you should be able to execute `justin version` to run the command and
get its built-in version number. This should be what you expect from looking
at the website. Sometimes the version in cvmfs might lag behind because
nothing has changed in the command script between justIN versions.

Next do `justin time` to contact the central justIN service and ask for the 
time in UTC. The first time you do this, you will be prompted to visit a
URL on the justIN website. Go there and follow the instructions to log in
with your Fermilab SSO account. `justin` creates a session file for you in
/var/tmp and has called ahead to the central service with details of that
session, which you authorize by folling that URL and logging in.

With this done, you can follow some of the simple commands in the 
[justIN DUNE tutorial](tutorials.dune.md) which do not need cvmfs. For
example: 

    justin simple-workflow --monte-carlo 10 --jobscript-id testpro:hello-world

will launch a test workflow, running a hello world jobscript 10 times.

If you are regularly using the `justin` command as a standalone script, you
should check for new versions periodically, especially if things stop
working as expected. Look for the version on the justIN dashboard page
footers, the output of `justin version`, and what's in GitHub or cvmfs.

