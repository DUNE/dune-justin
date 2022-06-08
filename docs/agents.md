## Agents

The Workflow System uses agents to make periodic updates to the 
[Workflow Database](database.md). 

Each agent is implemented as a self-contained daemon written in Python 3. A
systemd service file provided for each agent, and each agent writes to a log 
file in /var/log/wfs/ . 
For example, wfs-finder's log file is /var/log/wfs/finder .
 
- [wfs-info-collector](info-collector.md) - collects information about sites, storages, and users
- [wfs-finder](finder.md) - queries MetaCat for the list of files needed by a request and Rucio for the locations of each file's replicas
- [wfs-job-factory](job-factory.md) - submits generic jobs with jobsub, which query the Workflow Allocator to be allocated work

