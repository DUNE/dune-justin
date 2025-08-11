## External API rates

This page explains how often components of justIN call external services,
including Rucio and MetaCat. It is arranged by justIN service or agent, and
is kept in sync with the code of this version.

### Info Collector

The [justIN Info Collector](agents.info_collector.md) gathers information
from multiple external sources and records it in the justIN database. 

Like all justIN agents, processing is done in cycles and the Info Collector 
sleeps for 60 seconds between each cycle. Timers are maintained and checked 
during each cycle and the appropriate functions run.

The function **testRucio()** is run once every 300 seconds by default and
executes the function ping() of rucio.client.pingclient.PingClient() to use the
Rucio ping API three times to measure average Rucio responsiveness. 

The function **updateJwks()** is run once every 86400 seconds by default.
It calls https://cilogon.org/ to check the Well Known location for updated
JWKS keys.

The functions **updateStorages()**, 
**updateLogsDatasets()**,
**updateGroupsHTCondor()**, 
**updateGroupsWLCG()**  (which makes no external API calls)
and **updateScopes()** are run
together each 3600 seconds by default.

updateStorages() uses list_rses() of rucio.client.rseclient.RSEClient() to
get a list of RSEs known to Rucio, then for each RSE it uses
list_rse_attributes(), get_protocols(), and get_rse_usage(), and
get_account_limits() from rucio.client.accountclient.AccountClient() to
gather details of that RSE.

updateLogsDatasets() ensures that the current and next two log.tgz datasets 
exist for each RSE. Each dataset has a time range of one million seconds,
rounded down in units of one million seconds from the epoch. It checks if the 
datasets already exist using get_did() from 
rucio.client.didclient.DIDClient() and if not creates it in MetaCat by
executing the commands `metacat auth login` and `metacat dataset create` 
and then in Rucio with add_dataset(). For each dataset it also adds a rule with
add_replication_rule() from rucio.client.ruleclient.RuleClient() if after 
checking the dataset with list_replication_rules() it finds it has no rules.

updateGroupsHTCondor() runs the `condor_userprio -quotas -allusers` command 
to capture of list of current HTCondor groups.

updateScopes() runs list_scopes() and list_scopes_for_account() from
rucio.client.scopeclient.ScopeClient() to get details of all scopes and 
dunepro scopes.

The functions **updateSites()** and **updateSitesStorages()** (which
makes no external API calls) are run together each 3600 seconds by default.

updateSites() executes 
`git clone https://github.com/opensciencegrid/osg-gfactory.git` and then
parses the resulting XML and YAML files to populate the justIN database of
sites and entries. 

### Finder

### Job Factory 

### Wrapper jobs

### UI service

### Dashboard

 

