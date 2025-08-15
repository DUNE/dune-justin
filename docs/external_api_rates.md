## External API rates

This page explains how often components of justIN call external services,
including Rucio and MetaCat. It is arranged by justIN service or agent, and
is kept in sync with the code of this version.

### Create X509 Proxies

The justin-create-x509-proxies script is run each day from cron inside each
services/agents container. It runs voms-proxy-init twice to contact the
DUNE VOMS service and obtain VOMS proxies.

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

The [justIN Job Factory](agents.job_factory.md) decides whether to submit
justIN Wrapper Jobs to HTCondor.

Like all justIN agents, processing is done in cycles and the Job Factory
sleeps for 60 seconds between each cycle. Timers are maintained and checked 
during each cycle and the appropriate functions run.

Every 21600 seconds (6 hours) an AWT job is submitted targetted at each
site justIN is aware of using `condor_submit` to a HTCondor schedd randomly
chosen from all the schedds justIN is aware of.

Then the function ping() of rucio.client.pingclient.PingClient() of the
Rucio ping API is called three times to measure average Rucio responsiveness.
If sufficiently low, workflowJobs() is called which submits up to 2000 jobs
(in HTCondor clusters) in each cycle depending how many unallocated files
there are associated with activate workflows. 

### Wrapper jobs

Each wrapper job potentially makes multiple calls to MetaCat and Rucio but
only during the outputting phase. At the start of this phase, the job is 
supplied with a list of existing datasets created for this stage and known
to justIN. 

The job attempts to register the logs.tgz file with `metacat file declare`
up to three times. `metacat file show` is run to check the file is
registered. `justin-rucio-upload` is used to try to upload the file up to
three times with upload() of rucio.client.uploadclient.UploadClient() 
ADD TO DATASETS
RULES
CHECKS VIA RUCIO

The job creates a list of datasets it will need for outputting but removes
those which have already been created by other jobs. The maximal list in a
job is a per-RSE, per-pattern dataset within this stage, a numbered dataset 
for each pattern within this stage, and an overal dataset for this
stage and pattern. For each dataset that needs to be created, up to three
attempts are made to create the dataset with 
`justin-job-datasets` which also makes up to three attempts to create each
dataset with `metacat dataset create` and add_dataset() from
rucio.client.didclient.DIDClient() and add_replication_rule() from
rucio.client.ruleclient.RuleClient()

SIMILAR TO logs.tgz AS ABOVE

METACAT confirmed ETC AT EACH STEP

### UI service

The User Interface service only acts in response to requests from command
line clients initiated by users. 

The function showJobscriptCmd() calls https://raw.githubusercontent.com 
to fetch a jobscript using a GitHub path and tag.

The function showReplicasCmd() calls the MetaCat server to get a list of
files matching a given MQL query, and then uses list_replicas() from 
rucio.client.replicaclient.ReplicaClient() to get a list of replicas for
each file.

The function showFilesCmd() calls the MetaCat server to get a list of
files matching a given MQL query.

### Dashboard

The Dashboard service only acts in response to requests from web clients
initiated by users.

During logins, https://cilogon.org is called once to obtain tokens from 
CI Logon using OAuth2.

 

