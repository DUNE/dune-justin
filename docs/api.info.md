# justiN information API

This API is provided as URLs which can be fetched to export information
from the [justIN database](database.md) in CSV format.

## Scopes

[https://justin-ui-pro.dune.hep.ac.uk/api/info/scopes.csv](https://justin-ui-pro.dune.hep.ac.uk/api/info/scopes.csv)
gives a list of Rucio scopes and the DUNE WLCG Groups which have write
access to them through justIN.

## Sites

[https://justin-ui-pro.dune.hep.ac.uk/api/info/sites.csv](https://justin-ui-pro.dune.hep.ac.uk/api/info/sites.csv)
gives a list of DUNE Site Names and their enabled state as True/False.

## Storages

[https://justin-ui-pro.dune.hep.ac.uk/api/info/storages.csv](https://justin-ui-pro.dune.hep.ac.uk/api/info/storages.csv)
gives a list of
Rucio Storage Element names and their read and write states as True/False.

## Sites/storages distances

[https://justin-ui-pro.dune.hep.ac.uk/api/info/sites_storages.csv](https://justin-ui-pro.dune.hep.ac.uk/api/info/sites_storages.csv)
gives a 
list of DUNE Site Name, Rucio Storage Element name, the distance between
them in the range 0.0 to 1.0, the site's enabled state as True/False, and 
the RSE's read and write state as True/False. Storages which have no
entry for a particular site should be assumed to be inaccessible from that 
site.
