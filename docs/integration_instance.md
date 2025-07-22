# Integration instance

The justIN system relies on a central database and a set of agents and
services, including the web dashboard, which together constitute an 
*instance*. The DUNE production instance's dashboard has URL
[https://dunejustin.fnal.gov/dashboard/](https://dunejustin.fnal.gov/dashboard/)

## Production vs integration

To allow testing of new justIN releases with other components before they are
installed on the production instance, a DUNE *integration instance* is 
maintained with dashboard at 
[https://justin-int.dune.hep.ac.uk/dashboard/](https://justin-int.dune.hep.ac.uk/dashboard/)

Apart from the URL, the letters INT next to the j-clock near the top of the
page are a further visual cue that you are using the integration instance 
dashboard. The version is also displayed at the bottom of every page.

The justIN documentation is maintained in GitHub, versioned along with the 
code, and installed in the [docs area of the dashboard](./). For this reason,
you should consult the docs and [change log](CHANGELOG.md) for the instance
you are using (production or integration).

The integration instance is typically installed with a recent snapshot of the 
main branch in 
GitHub, taken while it is believed to be stable enough for testing. These 
updates may applied as frequently as daily or weekly depending on the phase of
development, and will generally be done between 08:00 and 12:00 UTC.

Each time a minor version (eg 01.01) is finished its testing and is installed
on the production instance, then the next minor version is started (eg 01.02)
and a clean install is made of the integration instance including wiping its
database. For this reason **it is essential that no important work is done 
using the integration instance.**

## Using the integration instance

The [justin command](justin_command.md) from the production version can
usually be used with the next version on the integration instance. This can
be accessed through cvmfs and setup in the usual way. If necessary, it is
also possible to do a [standalone installation](justin_command.standalone.md)
and the allows you to pick the integration version from the main branch.

Wherever the command is located, it is necessary to override the built-in
production instance URL with the `--url` option. For example:

    justin --url https://justin-ui-int.dune.hep.ac.uk/api/commands time

will give you the current time in UTC, according to the integration
instance.

For convenience, you can set the environment variable $JUSTIN_OPTIONS to
a string to be prepended to the list of command line options:

    export JUSTIN_OPTIONS='--url https://justin-ui-int.dune.hep.ac.uk/api/commands'
    justin time

Alternatively, you may prefer to define an alias in your shell profile,
as this makes it more explicit which instance you are connecting to. 
In Bash:

    alias justin-int='justin --url https://justin-ui-int.dune.hep.ac.uk/api/commands'
    justin-int time

## Workflow numbering

To avoid interfering with work done using the production instance, the
integration instance recycles the workflow IDs between 500 and 999. This 
number is reset every time the integration database it wiped and recreated.

