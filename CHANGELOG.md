# Changelog

## 01.05.00
- Allow file matching from jobs at NERSC to offsite storages

## 01.04.00
- Cache HTCondor log as jobs finish, retrying up to 10 times, and remove job 
  from HTCondor if log is successfully cached
- Dashboard offers live HTCondor log instead of cached for unfinished jobs
- Impose time limit on Finder cycles
- Support hierarchical HTCondor groups: group_dune.prod.mcsim etc
- Add overload_rucio_milliseconds setting to [agents] and suspend workflow
  job submission, new processing starts, and file allocations if Rucio is
  overloaded in Rucio ping test.
- Only last hour of activity used when deciding to pause workflows to 
  allow restarts 
- Add --instance and generalized instance support
- Add AWT GPU jobs at all sites with GPU entries

## 01.03.00
- Add finishing state to workflows and close Rucio datasets automatically
- justin get-token subcommand to fetch token and X.509 proxy from justIN
- Remove Pattern ID from WebDAV paths when uploading files to dCache
- NERSC GPU jobs now request a GPU
- Add --image to justin create-stage and simple-workflow to allow user to
  choose Apptainer image to use 
- Put a copy of https://kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js
  in root directory of dashboard website
- Export JUSTIN_MQL to jobscripts
- Add workflow.jobscript_max_rss_bytes to per file metadata
- Make justin-test-jobscript use justin get-token rather than user supplied
  VOMS proxy
- Remove voms-proxy-init from tutorial

## 01.02.00
- Add --gpu option to justin command, and direct jobs of GPU stages to 
  entries with GPUs, displaying GPU info on the job pages in the dashboard.
- Change maximum replica PFN length to 1024 in justindb.
- Add state_message to workflows, set in UI/Finder and displayed on dashboard
- Add justin-sl7-setup script to create a container in which to run
  commmands that need CentOS7/SL7 including ones that require UPS and setup.
- Change justin-cvmfs-upload to use Bearer Tokens not X.509 proxies
- Add symbolic links to /etc/justin-letsencrypt/* from /etc/letsencrypt/ for
  hardcoded assumptions
- Create destination datasets and per-RSE datasets on demand inside
  the wrapper jobs using justin-job-datasets helper script
- Create destination datasets of the form wXXXXsYpZnNNN in the wrapper job 
  where NNN is a counter to partition the datasets into 1000 file subsets. 
- Add an --output-rse-expression option for the justin command to allow
  a given RSE expression to be use when creating rules for all destination
  datasets.

## 01.01.00
- justin-prod-sched01.dune.hep.ac.uk and justin-prod-sched02.dune.hep.ac.uk
  included in defaults
- Event type IDs are generated using exec() from a list in __init__.py
- justin-check-db to be run when the justin-info-collector container starts
  and checks the event types in the code are also in the DB table event_types
- entry_has_gpus and always_has_gpus added to entries table in DB
- Add archived workflow pages
- Allow jobscripts to come from GitHub repos (DUNE/dist-comp#152)
- Automatic logs.tgz files created in 4M second per-RSE datasets which keep
  logs on the original RSE. Standalone justin-fetch-logs command added which
  uses Rucio client to fetch directly, and justin fetch-logs subcommand
  which fetches via justIN UI service without needing Rucio authentication
  (DUNE/dist-comp#137)
- Letsencrypt/certbot renewals done within justin-httpd container
  Files kept in /etc/justin-letsencrypt/ mounted from the host.
- Support for integration instance added
- MetaCat server URLs can now be set in the configuration
- MetaCat file info shown directly on justIN dashboard file pages
- Pages listing entries and showing status of an individual entry, including
  XML pilot factory configuration.
- Default Apptainer image for jobscripts can be given in configuration
- justin-rucio-upload can now check that Rucio has registered the file and
  added it to the given dataset.
- Jobscript Library has been retired and emphasis now on --jobscript-git
  in the man page, docs, and tutorial.
- Events listings have a form at the top to allow fine-grained filtering,
  and CSV and JSON downloads of events listings are available.
- HTCondor wrapper jobs require DUNE, LArSoft, and RCDS cvmfs mounts on
  worker nodes
- Fix bug DUNE/dist-comp#157 where unknown scope error generated another error
- RUCIO_ACCOUNT is set to dunepro in wrapper jobs 
- Per-stage lists of allowed RSEs for input files, output files, and sites
  at which to run.
- --seconds-needed option added to justin-get-file for multi-file jobscripts
- Add none_processed job state and events, and pausing of workflows if too
  many jobscript_error, or notused, or none_processed job outcomes.
  (DUNE/dist-comp#161)
- Add banner message from configuration
- In --output-pattern, the destination dataset is now optional, and a name
  like wXXXXsYpZ will be created if not given.
- Per-RSE datasets are created, each with a rule to keep the file on that
  RSE, and they are always used for Rucio uploads by jobs.
- Created datasets for output patterns have metadata describing the pattern,
  and stage parameters including the memory requested, Apptainer image etc.

## 01.00.00
- The "1.0" release of justIN after DC24
