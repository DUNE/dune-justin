## Agents

The Workflow System uses agents to make periodic updates to the 
[Workflow Database](database.md). 

Each agent is implemented as a self-contained daemon written in Python 3. A
systemd service file provided for each agent, writing to a log file in 
/var/log/wfs/ . For example, wfs-finder's log file is /var/log/wfs/finder .
 
### Agents

- wfs-info-collector - collects information about sites, storages, and users
- wfs-finder - queries MetaCat for the list of files needed by a request and Rucio for the locations of each file's replicas
- wfs-job-factory - submits generic jobs with jobsub, which query the [Workflow Allocator](workflow-allocator.md) to be allocated work

