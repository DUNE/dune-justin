## Agents

justIn uses agents to make periodic updates to the 
[justIn database](database.md). 

Each agent is implemented as a self-contained daemon written in Python 3. A
systemd service file provided for each agent, and each agent writes to a log 
file in /var/log/justin/ . 
For example, justin-finder's log file is /var/log/justin/finder .
 
- [justin-info-collector](info-collector.md) - collects information about sites, storages, and users
- [justin-finder](finder.md) - queries MetaCat for the list of files needed by a request and Rucio for the locations of each file's replicas
- [justin-stage-cache](stage-cache.md) - maintains the get_stage_cache and find_file_cache tables of currently optimal stages and unprocessed files for each site
- [justin-job-factory](job-factory.md) - submits generic jobs with jobsub, which query the Workflow Allocator service to be allocated work

