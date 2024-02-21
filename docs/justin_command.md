## justin command

The justin command allows the creation and monitoring of workflows, and 
various queries of the [justIN database](database.md)'s knowledge of
sites, storages etc.

See the [snapshot of its man page](justin_command.man_page.md) for the 
full list of subcommands, options, and their syntax.

On Fermilab dunegpvm machines and CERN's lxplus, it can easily be accessed
by setting up the usual DUNE environment and executing `setup justin` 

The command only requires Python 3.6 or above and has no dependencies 
beyond the standard Python 3 modules. 
Even on a macOS or Linux system without cvmfs, it should also be 
possible to 
[install and run](justin_command.standalone.md) the command standalone.

If you have Python2 module directories in $PYTHONPATH, it may be necessary
to unset PYTHONPATH in the session where you run the workflow command.

When first used on a given computer, the justin command contacts the central
justIN services and obtains a session ID and secret which are placed
in a temporary file. You will then be invited to visit a web page on the
justIN dashboard which has instructions on how to authorize that session,
using CILogon and your identity provider. Once authorized, you can use the
justin command on that computer for 7 days, and then you will be invited 
to re-authorize it. You can have multiple computers at multiple sites
authorized at the same time. 

The command `justin time` can be used to test the installation of the 
command and your registration with justIN. It contacts the
justIN central service, authenticates, and obtains the current time. 
