## Workflow command

The workflow command allows the creation and monitoring of requests, and 
various queries of the [Workflow Database](database.md)'s knowledge of
sites, storages etc.

See the [snapshot of its man page](workflow-man-page.md) for the full list
of subcommands, options, and their syntax.

The command requires Python 3.6 or above and has no dependencies beyond the
standard Python 3 modules. On a Linux system with python3 on the path, it
should be possible to install and run the workflow command directly from the
[commands directory in the Workflow System repo on GitHub](https://github.com/DUNE/dune-wfs/tree/main/commands).

If you have Python2 module directories in $PYTHONPATH, it may be necessary
to unset PYTHONPATH in the session where you run the workflow command.

To authenticate to the Workflow System, the command expects to be able to 
find a grid style X.509 proxy file in /tmp/x509up_uUUUU or in the file given
by $X509_USER_PROXY. VOMS extensions are not required but will be safely
ignored if present. 

The command `workflow time` can be used to test the installation of the 
command and your registration with the Workflow System. It contacts the
WFS central service, authenticates, and obtains the current time. 
