## External API rates

This page explains how often components of justIN call external services,
including Rucio and MetaCat. It is arranged by justIN service or agent, and
is kept in sync with the code of this version.

[TOC]

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

The [justIN Finder](agents.finder.md) finds jobs, files, and tokens in 
various states and performs necessary operations on them.

Like all justIN agents, processing is done in cycles and the Finder
sleeps for 60 seconds between each cycle. Timers are maintained and checked 
during each cycle and the appropriate functions run.

**findTokensToRefresh()** finds tokens expiring within the next hour which are
owned by users with active justIN sessions. For each token, it sends an
OIDC refresh request to CI Logon to obtain a new token.

Then the function ping() of rucio.client.pingclient.PingClient() of the
Rucio ping API is called three times to measure average Rucio responsiveness.
If the result is low enough, then findFiles() and findReplicas() are
executed.

For most workflows, where the input files are defined by a MQL query to
be evaluated once at the start, the **findFilesMetaCat()** function is used
to get a list of all input files for each workflow after it enters the
running state. For each workflow, three attempts are made with direct
HTTP REST requests to the MetaCat service. 

**findReplicas()** selects the highest priority workflow with
files still in the finding state, and then finds up to 500 files still in
the finding state and then uses list_replicas from 
rucio.client.replicaclient.ReplicaClient() to find the replicas of all
those files with a single call, first for the domain `wan` and then for
`lan`. 

**saveTerminalJobsLogs()** runs `condor_q` for each HTCondor scheduler to
obtain list of jobs' states. For jobs found to be in terminal states but
without saved HTCondor log files, `condor_transfer_data` and 
`condor_q -better` are run and the resulting log files saved to the justIN 
database. If this all succeeds, the job is removed from the spool with
`condor_rm`.

Every hour, **findStalledCondorJobs()** is run which runs `condor_q` for each
HTCondor scheduler to find a list of job states, and marks stalled jobs
in the justIN internal database.

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
there are associated with active workflows. 

### Wrapper jobs

Each wrapper job potentially makes multiple calls to MetaCat and Rucio but
only during the outputting phase. At the start of this phase, the job is 
supplied with a list of existing datasets created for this stage and known
to justIN. 

The job attempts to register the logs.tgz file with `metacat file declare`
up to three times. `metacat file show` is run to check the file is
registered. `justin-rucio-upload` is used to try to upload the file up to
three times with upload() of rucio.client.uploadclient.UploadClient() 

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

If the jobscript ends with success (0) then the output files it creates, 
identified by the patterns given when the stage was defined, are also
uploaded in a similar way to Rucio managed storage (or to scratch at Fermilab.)

For the log files and the output files to be uploaded to Rucio managed
storage, the same procedure is followed for each file. 


First, three attempts are made to register the file with Metacat, 
with `metacat file declare` . If the registration of the file fails
entirely, the job is aborted. Then `justin-rucio-upload` is used to
try to upload the file. This makes three attempts to upload the file 
and add it to one dataset with 
upload() from rucio.client.uploadclient.UploadClient(). If the upload
succeeds, the file is added to three more datasets using attach_dids()
from rucio.client.didclient.DIDClient(), trying each operation three times
and failing if the file cannot be added. Finally, list_replicas() from
rucio.client.replicaclient.ReplicaClient() 
list_files() rucio.client.didclient.DIDClient() 
are used to check the file has
been registered in Rucio and in the datasets 
to work around false reports of upload success
from Rucio. This check is tried three times and again overall failure
causes an abort.

For each file, `metacat dataset add-files` is then used to add files to
MetaCat datasets too. `metacat file update --metadata` is used to set 
dune.output_status=uploaded for the file, from the initial value of recorded.

After the wrapper job has reported the successful uploads to the justIN
Allocator Service and they have been recorded in the justIN database without
any conflicts (eg from duplicate/resubmitted jobs), then `metacat file update --metadata` is used to set 
dune.output_status=confirmed for each file.

### UI service

The User Interface service only acts in response to requests from command
line clients initiated by users. 

The function **showJobscriptCmd()** calls https://raw.githubusercontent.com 
to fetch a jobscript using a GitHub path and tag.

The function **showReplicasCmd()** calls the MetaCat server to get a list of
files matching a given MQL query, and then uses list_replicas() from 
rucio.client.replicaclient.ReplicaClient() to get a list of replicas for
each file.

The function **showFilesCmd()** calls the MetaCat server to get a list of
files matching a given MQL query.

### Dashboard

The Dashboard service only acts in response to requests from web clients
initiated by users.

During logins, https://cilogon.org is called once to obtain tokens from 
CI Logon using OAuth2.

### Per-file summary

This summary assumes a simple scenario of N files, each processed
by one job and producing one output file, with no failures or retries. 
Only per-file API call counts are included. For
example, the calls to create a datasets for thousands of files aren't included.
 
|Component  |API Call              |MetaCat|Rucio|HTCondor|
|-----------|----------------------|-------|-----|--------|
|Finder     |condor_q              |      0|    0|       1|
|Finder     |condor_transfer_data  |      0|    0|       1|
|Finder     |condor_rm             |      0|    0|       1|
|Wrapper Job|metacat file declare  |      2|    0|       0|
|Wrapper Job|upload()              |      0|    2|       0|
|Wrapper Job|attach_dids()         |      0|    4|       0|
|Wrapper Job|metacat dataset add-files|   4|    0|       0|
|Wrapper Job|metacat file update   |      2|    0|       0|
